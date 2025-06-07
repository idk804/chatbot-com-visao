import g4f
import gradio as gr

# Modelos com suporte a visão
MODELOS = [
    "gpt-4o",
    "gpt-4.1",
    "claude-3.7-sonnet",
    "claude-3.7-sonnet-thinking",
]

# Função principal que envia o prompt e imagens ao modelo
def gerar_resposta(prompt, modelo, imagens):
    try:
        client = g4f.Client(provider=g4f.Provider.LegacyLMArena)

        imagens_formatadas = []
        if imagens:
            for img in imagens:
                imagens_formatadas.append([img, img.name])

        resposta = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            images=imagens_formatadas
        )

        return resposta.choices[0].message.content

    except Exception as erro:
        return f"Erro: {erro}"

# Interface Gradio
with gr.Blocks() as app:
    gr.Markdown("## 🤖 Chatbot com Visão - G4F\n**Feito por Gabriel Organista**")

    with gr.Row():
        prompt = gr.Textbox(label="Escreva seu prompt", lines=2, placeholder="Ex: O que tem nessa imagem?")
        modelo = gr.Dropdown(label="Escolha o modelo", choices=MODELOS, value=MODELOS[0])

    imagens = gr.File(label="Envie uma ou mais imagens", file_types=["image"], file_count="multiple")
    botao = gr.Button("Enviar")

    resposta = gr.Textbox(label="Resposta", lines=10)

    botao.click(fn=gerar_resposta, inputs=[prompt, modelo, imagens], outputs=resposta)

# Lançar app no servidor do Fly
app.launch(server_name="0.0.0.0", server_port=8080)
