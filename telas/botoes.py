import gradio as gr


def criar_botao(html):
    return gr.HTML(
        value=html,
        apply_default_css=False,
        elem_classes="acao-tela",
        js_on_load="element.querySelector('button').addEventListener('click', () => trigger('click'));",
    )
