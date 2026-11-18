
import gradio as gr
from dados.entregas import entregas


def criar_tela_entregas():

    gr.Markdown("## Entregas em andamento")

    gr.Markdown("Selecione uma entrega para visualizar sua rota.")

    opcoes = []

    for entrega in entregas:
        texto = (
            f"Entrega #{entrega['id']} | "
            f"{entrega['origem']} → {entrega['destino']}"
        )
        opcoes.append(texto)

    lista_entregas = gr.Radio(
        choices=opcoes,
        label="Suas entregas"
    )

    return lista_entregas
