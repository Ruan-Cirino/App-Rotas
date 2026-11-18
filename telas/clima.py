import requests

def consultar_clima():
    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": -25.4284,
        "longitude": -49.2733,
        "current": [
            "temperature_2m",
            "precipitation",
            "wind_speed_10m"
        ],
        "timezone": "America/Sao_Paulo"
    }

    resposta = requests.get(url, params=parametros)
    dados = resposta.json()

    print("===== CLIMA ATUAL =====")
    print("Temperatura:", dados["current"]["temperature_2m"], "°C")
    print("Chuva:", dados["current"]["precipitation"], "mm")
    print("Vento:", dados["current"]["wind_speed_10m"], "km/h")


if __name__ == "__main__":
    consultar_clima()