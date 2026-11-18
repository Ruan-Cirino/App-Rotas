
import gradio as gr

<<<<<<< HEAD
from telas.botoes import criar_botao

=======
>>>>>>> 0b5b2d468018a7c962ca3bef17a315f5cfab7d95
# responsável por construir a tela inicial
def criar_tela_inicio():

    gr.Markdown("# Rotas")

    gr.Markdown("## Painel do Entregador")

    gr.Markdown(
        "Bem-vindo ao Rotas! "
        "Gerencie suas entregas, consulte rotas "
        "e acompanhe a previsão do tempo."
    )

<<<<<<< HEAD
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
=======
    botao_entregas = gr.Button(
        "Ver Entregas",
        variant="primary"
    )
>>>>>>> 0b5b2d468018a7c962ca3bef17a315f5cfab7d95

    return botao_entregas
