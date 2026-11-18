
import gradio as gr

from telas.botoes import criar_botao

# responsável por construir a tela inicial
def criar_tela_inicio():

    gr.Markdown("# Rotas")

    gr.Markdown("## Painel do Entregador")

    gr.Markdown(
        "Bem-vindo ao Rotas! "
        "Gerencie suas entregas, consulte rotas "
        "e acompanhe a previsão do tempo."
    )

    botao_entregas = criar_botao("""
        <button type="button" class="botao-entregas">
            <span>Ver Entregas</span>
            <svg aria-hidden="true" focusable="false" viewBox="0 0 41 24">
                <polygon points="2,4 7,4 16,12 7,20 2,20 11,12" />
                <polygon points="13,4 18,4 27,12 18,20 13,20 22,12" />
                <polygon points="24,4 29,4 38,12 29,20 24,20 33,12" />
            </svg>
        </button>
    """)

    return botao_entregas
