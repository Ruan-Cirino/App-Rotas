
import gradio as gr

# responsável por construir a tela inicial
def criar_tela_inicio():

    gr.Markdown("# Rotas")

    gr.Markdown("## Painel do Entregador")

    gr.Markdown(
        "Bem-vindo ao Rotas! "
        "Gerencie suas entregas, consulte rotas "
        "e acompanhe a previsão do tempo."
    )

    botao_entregas = gr.Button(
        "Ver Entregas",
        variant="primary"
    )

    return botao_entregas
