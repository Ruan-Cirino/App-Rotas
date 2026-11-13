
import gradio as gr

from telas.inicio import criar_tela_inicio
from telas.entregas import criar_tela_entregas
from telas.rotas import criar_tela_rota, carregar_mapa


# Criando o aplicativo
with gr.Blocks(title="MotoRoute") as app:

    # Tela inicial
    with gr.Column(visible=True) as tela_inicio:
        botao_entregas = criar_tela_inicio()

    # Tela de entregas
    with gr.Column(visible=False) as tela_entregas:
        lista_entregas = criar_tela_entregas()
        botao_voltar_inicio = gr.Button("Voltar")

    # Tela da rota
    with gr.Column(visible=False) as tela_rota:
        mapa, botao_voltar_entregas = criar_tela_rota()

    # Abrir a tela de entregas
    def abrir_entregas():
        return gr.update(visible=False), gr.update(visible=True)

    # Voltar para a tela inicial
    def voltar_inicio():
        return gr.update(visible=True), gr.update(visible=False)

    # Abre a tela da rota e carrega o mapa
    def abrir_rota(entrega_selecionada):

        if entrega_selecionada is None:
            gr.Warning("Selecione uma entrega primeiro!")
            return gr.update(), gr.update(), gr.update()

        try:
            html_mapa = carregar_mapa(entrega_selecionada)

            return (
                gr.update(visible=False),
                gr.update(visible=True),
                html_mapa
            )

        except Exception as erro:
            gr.Warning(f"Erro ao carregar mapa: {erro}")
            return gr.update(), gr.update(), gr.update()


    # Voltar para a lista de entregas
    def voltar_entregas():
        return gr.update(visible=True), gr.update(visible=False)

    # Eventos dos botões
    botao_entregas.click(
        fn=abrir_entregas,
        outputs=[tela_inicio, tela_entregas]
    )

    botao_voltar_inicio.click(
        fn=voltar_inicio,
        outputs=[tela_inicio, tela_entregas]
    )

    # Ao selecionar uma entrega, abre a tela da rota

    lista_entregas.change(
        fn=abrir_rota,
        inputs=lista_entregas,
        outputs=[tela_entregas, tela_rota, mapa]
    )


    botao_voltar_entregas.click(
        fn=voltar_entregas,
        outputs=[tela_entregas, tela_rota]
    )


# Iniciando o aplicativo
if __name__ == "__main__":
    app.launch()
