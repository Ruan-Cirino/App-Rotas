
import requests
import math

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


FUSO = ZoneInfo("America/Sao_Paulo")

URL_OPEN_METEO = "https://api.open-meteo.com/v1/forecast"


CODIGOS_CLIMA = {
    0: "Céu limpo",
    1: "Predominantemente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Neblina",
    48: "Neblina com geada",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa intensa",
    61: "Chuva leve",
    63: "Chuva moderada",
    65: "Chuva forte",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    80: "Pancadas de chuva",
    81: "Pancadas moderadas",
    82: "Pancadas fortes",
    95: "Trovoadas",
    96: "Trovoadas com granizo",
    99: "Trovoadas intensas"
}


def calcular_distancia(ponto_a, ponto_b):
    """Calcula a distância entre dois pontos usando Haversine."""

    lat1, lon1 = map(math.radians, ponto_a)
    lat2, lon2 = map(math.radians, ponto_b)

    diferenca_lat = lat2 - lat1
    diferenca_lon = lon2 - lon1

    a = (
        math.sin(diferenca_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(diferenca_lon / 2) ** 2
    )

    return 6371000 * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )


def selecionar_pontos_rota(coordenadas):
    """Seleciona origem, dois pontos intermediários e destino."""

    if len(coordenadas) < 2:
        raise ValueError("A rota não possui coordenadas suficientes.")

    distancias = [0]

    for i in range(1, len(coordenadas)):
        trecho = calcular_distancia(
            coordenadas[i - 1],
            coordenadas[i]
        )

        distancias.append(distancias[-1] + trecho)

    distancia_total = distancias[-1]

    if distancia_total == 0:
        raise ValueError("Não foi possível calcular a distância da rota.")

    pontos = []

    for fracao in (0, 1 / 3, 2 / 3, 1):
        distancia_alvo = distancia_total * fracao

        indice = min(
            range(len(distancias)),
            key=lambda i: abs(distancias[i] - distancia_alvo)
        )

        ponto = coordenadas[indice]

        if not pontos or ponto != pontos[-1]:
            pontos.append(ponto)

    return pontos


def consultar_previsao_ponto(latitude, longitude, horario):
    """Consulta a previsão horária para um ponto da rota."""

    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": (
            "temperature_2m,"
            "precipitation_probability,"
            "precipitation,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "timezone": "America/Sao_Paulo",
        "forecast_days": 7
    }

    resposta = requests.get(
        URL_OPEN_METEO,
        params=parametros,
        timeout=15
    )

    resposta.raise_for_status()

    dados = resposta.json()

    if "hourly" not in dados:
        raise ValueError("Previsão meteorológica indisponível.")

    horarios = dados["hourly"]["time"]

    horario_alvo = horario.strftime("%Y-%m-%dT%H:00")

    indice = min(
        range(len(horarios)),
        key=lambda i: abs(
            (
                datetime.fromisoformat(horarios[i]) - horario.replace(
                    tzinfo=None,
                    minute=0,
                    second=0,
                    microsecond=0
                )
            ).total_seconds()
        )
    )

    horario_encontrado = datetime.fromisoformat(horarios[indice])

    diferenca = abs(
        (horario_encontrado - horario.replace(tzinfo=None)).total_seconds()
    )

    if diferenca > 5400:
        return None

    previsao = dados["hourly"]

    def valor(campo):
        return previsao[campo][indice]

    codigo = valor("weather_code")

    return {
        "horario": horario_alvo,
        "temperatura": valor("temperature_2m"),
        "probabilidade": valor("precipitation_probability"),
        "chuva": valor("precipitation"),
        "vento": valor("wind_speed_10m"),
        "condicao": CODIGOS_CLIMA.get(
            codigo,
            "Condição desconhecida"
        )
    }


def prever_clima_rota(coordenadas, duracao_segundos, horario_saida=None):
    """
    Combina a duração da rota com a previsão climática
    nos horários estimados de passagem.
    """

    if horario_saida is None:
        horario_saida = datetime.now(FUSO)

    elif horario_saida.tzinfo is None:
        horario_saida = horario_saida.replace(tzinfo=FUSO)

    pontos = selecionar_pontos_rota(coordenadas)

    previsoes = []

    for indice, ponto in enumerate(pontos):

        fracao = indice / max(len(pontos) - 1, 1)

        horario_passagem = horario_saida + timedelta(
            seconds=duracao_segundos * fracao
        )

        try:
            clima = consultar_previsao_ponto(
                ponto[0],
                ponto[1],
                horario_passagem
            )

        except requests.RequestException:
            clima = None

        previsoes.append({
            "local": (
                "Origem" if indice == 0
                else "Destino" if indice == len(pontos) - 1
                else f"Trecho intermediário {indice}"
            ),
            "horario_estimado": horario_passagem.strftime("%H:%M"),
            "clima": clima
        })

    return {
        "saida": horario_saida.strftime("%d/%m/%Y %H:%M"),
        "chegada": (
            horario_saida + timedelta(seconds=duracao_segundos)
        ).strftime("%d/%m/%Y %H:%M"),
        "duracao_minutos": round(duracao_segundos / 60),
        "pontos": previsoes
    }
