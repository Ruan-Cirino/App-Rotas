
import gradio as gr
from html import escape

from servicos.mapas import criar_mapa
<<<<<<< HEAD
from telas.botoes import criar_botao
=======
>>>>>>> 0b5b2d468018a7c962ca3bef17a315f5cfab7d95



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
<<<<<<< HEAD
        title="Mapa da rota"
=======
        style="border: none; border-radius: 12px;"
>>>>>>> 0b5b2d468018a7c962ca3bef17a315f5cfab7d95
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
<<<<<<< HEAD
        value="<p>Carregando mapa...</p>",
        elem_classes="mapa-rota"
    )

    # Botão para voltar
    texto = "<span>Voltar</span> <span>às</span> <span>entregas</span>"
    botao_voltar = criar_botao(f"""
        <button type="button" class="botao-voltar-entregas" aria-label="Voltar às entregas">
            <span class="text" aria-hidden="true">{texto}</span>
            <span class="clone" aria-hidden="true">{texto}</span>
            <svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 19V5M6 11l6-6 6 6" />
            </svg>
        </button>
    """)
=======
        value="<p>Carregando mapa...</p>"
    )

    # Botão para voltar
    botao_voltar = gr.Button("Voltar às entregas")
>>>>>>> 0b5b2d468018a7c962ca3bef17a315f5cfab7d95

    return mapa, botao_voltar
