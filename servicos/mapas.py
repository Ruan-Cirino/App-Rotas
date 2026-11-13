
import folium
import requests



def criar_mapa(origem=None, destino=None):

    # Coordenadas padrão para testar o mapa
    if origem is None:
        origem = [-25.4284, -49.2733]

    if destino is None:
        destino = [-25.4417, -49.2900]


    # Endereço da API OSRM
    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{origem[1]},{origem[0]};"
        f"{destino[1]},{destino[0]}"
        "?overview=full&geometries=geojson&steps=true"
    )

    # Consultando a API
    resposta = requests.get(url, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()

    if dados.get("code") != "Ok" or not dados.get("routes"):
        raise ValueError("Não foi possível calcular a rota.")

    # Pegando a primeira rota encontrada
    rota = dados["routes"][0]

    # Percorrendo os trechos da rota
    for trecho in rota["legs"]:

        # Percorrendo cada instrução do trajeto
        for passo in trecho["steps"]:

            rua = passo.get("name") or "Rua sem nome"
            distancia = passo["distance"]
            
            # Traduzindo os tipos de manobra
            traducoes = {
                "depart": "Iniciar trajeto",
                "turn": "Virar",
                "end of road": "Fim da rua",
                "new name": "Continuar pela via",
                "continue": "Seguir em frente",
                "arrive": "Chegou ao destino"
            }

            tipo = passo["maneuver"]["type"]

            manobra = traducoes.get(tipo, tipo)


            print(
                f"{manobra} | {rua} | {distancia:.0f} metros"
            )

    # Convertendo coordenadas para o formato do Folium
    coordenadas = [
        [latitude, longitude]
        for longitude, latitude in rota["geometry"]["coordinates"]
    ]

    # Criando o mapa
    mapa = folium.Map(
        location=origem,
        zoom_start=13,
        zoom_control="topright"
    )

    # Painel de instruções de navegação
    instrucoes_html = """
    <div style="
        position: fixed;
        top: 20px;
        left: 20px;
        width: 300px;
        max-height: 75vh;
        overflow-y: auto;
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px #888;
        z-index: 9999;
        font-family: Arial;
    ">
        <h3>Instruções da rota</h3>
    """

    for trecho in rota["legs"]:
        for passo in trecho["steps"]:
            rua = passo.get("name") or "Rua sem nome"
            distancia = passo["distance"]
            tipo = passo["maneuver"]["type"]

            traducoes = {
                "depart": "Iniciar trajeto",
                "turn": "Virar",
                "end of road": "Fim da rua",
                "new name": "Continuar",
                "continue": "Seguir em frente",
                "arrive": "Chegada"
            }

            manobra = traducoes.get(tipo, tipo)

            instrucoes_html += (
                f"<p><b>{manobra}</b><br>"
                f"{rua} — {distancia:.0f} metros</p><hr>"
            )

    instrucoes_html += "</div>"

    # Adicionando o painel ao mapa
    mapa.get_root().html.add_child(
        folium.Element(instrucoes_html)
    )


    # Marcador de origem
    folium.Marker(
        location=origem,
        popup="Centro de Curitiba",
        tooltip="Partida",
        icon=folium.Icon(color="green")
    ).add_to(mapa)

    # Marcador de destino
    folium.Marker(
        location=destino,
        popup="Batel, Curitiba",
        tooltip="Chegada",
        icon=folium.Icon(color="red")
    ).add_to(mapa)

    # Desenhando o trajeto pelas ruas
    folium.PolyLine(
        locations=coordenadas,
        color="blue",
        weight=6,
        opacity=0.8
    ).add_to(mapa)

    # Ajustando o mapa ao percurso
    mapa.fit_bounds(coordenadas)

    # Calculando distância e duração
    distancia = rota["distance"] / 1000
    duracao = rota["duration"] / 60

    print(f"Distância: {distancia:.2f} km")
    print(f"Tempo estimado: {duracao:.0f} minutos")

    # Salvando o mapa
    mapa.save("mapa_teste.html")

    # Devolve o HTML completo do mapa
    return mapa.get_root().render()



if __name__ == "__main__":
    criar_mapa()
