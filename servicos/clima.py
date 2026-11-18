
import requests
from statistics import mean
from collections import Counter


def consultar_clima(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "precipitation,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "hourly": "precipitation_probability",
        "timezone": "America/Sao_Paulo",
        "forecast_days": 1
    }

    resposta = requests.get(
        url,
        params=parametros,
        timeout=15
    )

    resposta.raise_for_status()

    dados = resposta.json()

    if "current" not in dados:
        raise ValueError("Dados meteorológicos indisponíveis.")

    atual = dados["current"]

    # Identificando a probabilidade de chuva na hora atual
    horarios = dados["hourly"]["time"]
    probabilidades = dados["hourly"]["precipitation_probability"]

    horario_atual = atual["time"][:13] + ":00"

    try:
        indice = horarios.index(horario_atual)
        probabilidade = probabilidades[indice]
    except ValueError:
        probabilidade = None

    # Traduzindo os códigos meteorológicos
    codigos = {
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

    codigo = atual["weather_code"]

    return {
        "temperatura": atual["temperature_2m"],
        "chuva": atual["precipitation"],
        "vento": atual["wind_speed_10m"],
        "probabilidade": probabilidade,
        "condicao": codigos.get(codigo, "Condição desconhecida")
    }


# =====================================
# CALCULAR MÉDIA CLIMÁTICA DA ROTA
# =====================================

def consultar_clima_medio(pontos):

    resultados = []

    # Consultando o clima dos pontos da rota
    for ponto in pontos:

        clima = consultar_clima(
            ponto[0],
            ponto[1]
        )

        resultados.append(clima)

    # Calcula a média ignorando valores indisponíveis
    def calcular_media(campo):

        valores = [
            resultado[campo]
            for resultado in resultados
            if resultado[campo] is not None
        ]

        if not valores:
            return None

        return round(mean(valores), 1)

    # Identifica a condição mais frequente
    condicoes = [
        resultado["condicao"]
        for resultado in resultados
        if resultado["condicao"] != "Condição desconhecida"
    ]

    if condicoes:
        condicao_media = Counter(condicoes).most_common(1)[0][0]
    else:
        condicao_media = "Indisponível"

    return {
        "temperatura": calcular_media("temperatura"),
        "chuva": calcular_media("chuva"),
        "vento": calcular_media("vento"),
        "probabilidade": calcular_media("probabilidade"),
        "condicao": condicao_media
    }
