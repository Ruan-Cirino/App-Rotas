
import folium
import requests
from html import escape
from servicos.clima import consultar_clima_medio


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

    
    # =====================================
    # INSTRUÇÕES DA ROTA
    # =====================================

    instrucoes_html = ""
    primeira_instrucao = True

    direcoes = {
        "uturn": "Faça o retorno",
        "sharp right": "bruscamente à direita",
        "right": "à direita",
        "slight right": "levemente à direita",
        "straight": "em frente",
        "slight left": "levemente à esquerda",
        "left": "à esquerda",
        "sharp left": "bruscamente à esquerda"
    }

    icones = {
        "uturn": "↶",
        "sharp right": "↱",
        "right": "→",
        "slight right": "↗",
        "straight": "↑",
        "slight left": "↖",
        "left": "←",
        "sharp left": "↰"
    }

    def formatar_distancia(metros):
        if metros >= 1000:
            return f"{metros / 1000:.1f}".replace(".", ",") + " km"
        return f"{metros:.0f} m"

    for trecho in rota["legs"]:
        for passo in trecho["steps"]:

            manobra = passo["maneuver"]
            tipo = manobra.get("type", "")
            modificador = manobra.get("modifier", "")

            rua = passo.get("name") or ""
            distancia_passo = passo.get("distance", 0)

            direcao = direcoes.get(modificador, "")

            if tipo == "depart":
                acao = "Inicie o trajeto"

            elif tipo == "arrive":
                acao = "Você chegou ao destino"

            elif tipo == "turn":
                acao = (
                    direcao if modificador == "uturn"
                    else f"Vire {direcao}" if direcao
                    else "Faça a conversão"
                )

            elif tipo == "end of road":
                acao = f"No fim da rua, vire {direcao}" if direcao else "Siga até o fim da rua"

            elif tipo == "continue":
                acao = f"Continue {direcao}" if direcao else "Siga em frente"

            elif tipo == "new name":
                acao = "Continue pela via"

            elif tipo == "merge":
                acao = "Incorpore-se à via"

            elif tipo == "on ramp":
                acao = "Acesse a alça de entrada"

            elif tipo == "off ramp":
                acao = "Pegue a saída"

            elif tipo == "fork":
                acao = f"Na bifurcação, siga {direcao}" if direcao else "Siga pela bifurcação"

            elif tipo in ("roundabout", "rotary"):
                acao = "Entre na rotatória"

            elif tipo == "roundabout turn":
                acao = f"Na rotatória, siga {direcao}" if direcao else "Siga pela rotatória"

            elif tipo in ("exit roundabout", "exit rotary"):
                acao = "Saia da rotatória"

            else:
                acao = "Continue o trajeto"

            icone = icones.get(
                modificador,
                "◎" if tipo == "arrive" else "↑"
            )

            classe = "item-rota destaque" if primeira_instrucao else "item-rota"

            etiqueta = (
                '<small>INÍCIO DA ROTA</small>'
                if primeira_instrucao else ""
            )

            primeira_instrucao = False

            rua_html = (
                f'<p class="detalhe-rota">{escape(rua)}</p>'
                if rua else ""
            )

            distancia_html = (
                f'<span class="distancia-rota">{formatar_distancia(distancia_passo)}</span>'
                if distancia_passo > 0 else ""
            )

            instrucoes_html += f"""
                <div class="{classe}">
                    <div class="icone-rota">{icone}</div>

                    <div class="conteudo-rota">
                        {etiqueta}
                        <b>{escape(acao)}</b>
                        {rua_html}
                        {distancia_html}
                    </div>
                </div>
            """


    # =====================================
    # INFORMAÇÕES CLIMÁTICAS
    # =====================================

    
    # =====================================
    # RESUMO CLIMÁTICO DA ROTA
    # =====================================

    pontos_climaticos = [
        coordenadas[0],
        coordenadas[len(coordenadas) // 2],
        coordenadas[-1]
    ]

    try:

        clima = consultar_clima_medio(pontos_climaticos)

        temperatura = (
            f"{clima['temperatura']} °C"
            if clima["temperatura"] is not None
            else "Indisponível"
        )

        chuva = (
            f"{clima['chuva']} mm"
            if clima["chuva"] is not None
            else "Indisponível"
        )

        vento = (
            f"{clima['vento']} km/h"
            if clima["vento"] is not None
            else "Indisponível"
        )

        probabilidade = (
            f"{clima['probabilidade']}%"
            if clima["probabilidade"] is not None
            else "Indisponível"
        )

        clima_html = f"""
            <div class="item-clima">

                <p>🌡️ Temperatura média: <b>{temperatura}</b></p>

                <p>🌧️ Chuva média: <b>{chuva}</b></p>

                <p>☔ Probabilidade média: <b>{probabilidade}</b></p>

                <p>💨 Vento médio: <b>{vento}</b></p>

                <p>🌤️ Condição predominante:
                    <b>{escape(str(clima['condicao']))}</b>
                </p>

            </div>
        """

    except Exception as erro:

        print(f"Erro ao consultar clima da rota: {erro}")

        clima_html = """
            <div class="item-clima">
                <p>Informações climáticas indisponíveis.</p>
            </div>
        """

    # =====================================
    # PAINÉIS MINIMALISTAS
    # =====================================

    paineis_html = f"""
    <style>

        
        
        * {{
            box-sizing: border-box;
        }}

        .controles-mapa {{
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 10000;
            display: flex;
            gap: 8px;
            font-family: Arial, sans-serif;
        }}

        .botao-mapa {{
            border: 1px solid #e5e7eb;
            background: #ffffff;
            color: #222222;
            padding: 10px 14px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: background 0.2s;
        }}

        .botao-mapa:hover {{
            background: #f1f5f9;
        }}

        .painel-mapa {{
            display: none;
            position: fixed;
            top: 65px;
            left: 15px;
            width: 320px;
            max-width: calc(100vw - 30px);
            max-height: 75vh;
            overflow-y: auto;
            background: #ffffff;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.18);
            z-index: 9999;
            font-family: Arial, sans-serif;
            color: #222222;
        }}

        .painel-mapa h3 {{
            margin: 0 0 15px;
            padding-bottom: 12px;
            border-bottom: 1px solid #eeeeee;
            font-size: 17px;
            font-weight: 600;
        }}

        .fechar-painel {{
            float: right;
            border: none;
            background: transparent;
            font-size: 22px;
            cursor: pointer;
            color: #777777;
        }}

        /* INSTRUÇÕES */

        .item-rota {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 14px 4px;
            border-bottom: 1px solid #eeeeee;
            font-size: 13px;
        }}

        .icone-rota {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #f1f3f5;
            color: #333333;
            font-size: 19px;
            font-weight: bold;
        }}

        .conteudo-rota {{
            flex: 1;
            min-width: 0;
        }}

        .conteudo-rota b {{
            display: block;
            font-size: 14px;
            color: #222222;
            line-height: 1.4;
        }}

        .detalhe-rota {{
            margin: 4px 0;
            color: #666666;
            font-size: 12px;
        }}

        .distancia-rota {{
            display: inline-block;
            margin-top: 4px;
            color: #777777;
            font-size: 11px;
        }}

        .item-rota.destaque {{
            background: #f4f7ff;
            border: 1px solid #dce6ff;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 8px;
        }}

        .item-rota.destaque .icone-rota {{
            background: #2563eb;
            color: white;
        }}

        .item-rota.destaque small {{
            display: block;
            color: #2563eb;
            font-size: 10px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        /* CLIMA */

        .item-clima {{
            padding: 8px 0;
            font-size: 13px;
        }}

        .item-clima p {{
            margin: 12px 0;
            color: #444444;
        }}

        @media (max-width: 600px) {{
            .painel-mapa {{
                width: calc(100vw - 30px);
                max-height: 65vh;
            }}
        }}

    </style>

    <!-- Botões de controle -->
    <div class="controles-mapa">

        <button class="botao-mapa"
                onclick="alternarPainel('painel-instrucoes')">
            ☰ Instruções
        </button>

        <button class="botao-mapa"
                onclick="alternarPainel('painel-clima')">
            🌤 Clima
        </button>

    </div>

    <!-- Painel de instruções -->
    <div id="painel-instrucoes" class="painel-mapa">

        <button class="fechar-painel"
                onclick="fecharPaineis()">
            ×
        </button>

        <h3>Instruções da rota</h3>

        {instrucoes_html}

    </div>

    <!-- Painel climático -->
    <div id="painel-clima" class="painel-mapa">

        <button class="fechar-painel"
                onclick="fecharPaineis()">
            ×
        </button>

        <h3>🌤️ Clima da rota</h3>

        {clima_html}

    </div>

    <!-- Controle dos painéis -->
    <script>

        function fecharPaineis() {{

            document.getElementById(
                'painel-instrucoes'
            ).style.display = 'none';

            document.getElementById(
                'painel-clima'
            ).style.display = 'none';

        }}

        function alternarPainel(id) {{

            const painel = document.getElementById(id);

            const estavaAberto = painel.style.display === 'block';

            fecharPaineis();

            if (!estavaAberto) {{
                painel.style.display = 'block';
            }}

        }}

    </script>
    """

    mapa.get_root().html.add_child(
        folium.Element(paineis_html)
    )

    # =====================================
    # MARCADORES
    # =====================================

    folium.Marker(
        location=origem,
        popup="Centro de Curitiba",
        tooltip="Partida",
        icon=folium.Icon(color="green")
    ).add_to(mapa)

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

    # =====================================
    # DISTÂNCIA E DURAÇÃO
    # =====================================

    distancia = rota["distance"] / 1000
    duracao = rota["duration"] / 60

    print(f"Distância: {distancia:.2f} km")
    print(f"Tempo estimado: {duracao:.0f} minutos")

    # Salvando o mapa
    mapa.save("mapa_teste.html")

    # Devolve o HTML completo
    return mapa.get_root().render()


if __name__ == "__main__":
    criar_mapa()
