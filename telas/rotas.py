
import gradio as gr
from html import escape

from servicos.mapas import criar_mapa



def carregar_mapa(entrega_selecionada):

    # Importando nosso vetor de entregas
    from dados.entregas import entregas

    # Procurando a entrega selecionada
    for entrega in entregas:

        identificacao = f"Entrega #{entrega['id']} |"

        if entrega_selecionada.startswith(identificacao):

            origem = entrega["coord_origem"]
            destino = entrega["coord_destino"]

            # Criando o mapa da entrega escolhida
            html_mapa = criar_mapa(origem, destino)

            break

    else:
        raise ValueError("Entrega não encontrada!")

    # Coloca o mapa dentro de um iframe
    iframe = f"""
    <iframe
        srcdoc="{escape(html_mapa, quote=True)}"
        width="100%"
        height="600"
        style="border: none; border-radius: 12px;"
    ></iframe>
    """

    return iframe


# Função responsável pela tela da rota
def criar_tela_rota():

    gr.Markdown("##  Rota da Entrega")

    gr.Markdown(
        "Visualize o trajeto e as instruções de navegação."
    )

    # Espaço para exibir o mapa
    mapa = gr.HTML(
        value="<p>Carregando mapa...</p>"
    )

    # Botão para voltar
    botao_voltar = gr.Button("Voltar às entregas")

    return mapa, botao_voltar
