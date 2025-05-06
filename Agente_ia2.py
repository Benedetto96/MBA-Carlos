import streamlit as st
from openai import OpenAI
from datetime import datetime

# Inicializar cliente da DeepSeek
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key="sk-c938cc23f532438e8f0cc3de62a9c786",
)

# Configuração do Streamlit
st.set_page_config(page_title="Gerador de Conteúdo - Thais Galassi", layout="wide")
st.title("🎙️ Gerador de Conteúdo para o Podcast da Thais Galassi")

# Segmentador de tema
temas = ["Espiritualidade", "Saúde e Bem-estar", "Meditação", "Religião", "Todos os temas"]
tema = st.selectbox("Escolha o tema do conteúdo:", temas)

# Estado da sessão
if "conteudo_atual" not in st.session_state:
    st.session_state["conteudo_atual"] = None
if "historico" not in st.session_state:
    st.session_state["historico"] = []

# Geração do prompt
def gerar_prompt(tema):
    data_atual = datetime.now().strftime("%d/%m/%Y")
    return f"""
Você é um criador de conteúdo para a Thais Galassi, especialista em {tema}. Crie um roteiro de podcast com duração de 23 minutos (aproximadamente 116 linhas de conteúdo).

Regras:
- Crie um tema inovador, profundo, impactante e atual, com base em movimentos emocionais ou sociais relevantes do Brasil ou do mundo, relacionados ao tema.
- As primeiras 16 linhas devem ser um resumo com título "RESUMO" antes do texto.
- As 100 linhas seguintes devem ser o texto principal com título "TEXTO COMPLETO" antes do conteúdo.
- Use frases que emocionam, que conectam com a dor e a esperança humana.
- Aprofunde conceitos de forma prática, espiritual, acolhedora e transformadora.
- Insira pelo menos 2 citações reais e inspiradoras de autores ou pensadores.
- Fale como a Thais: com doçura, firmeza, profundidade e fé.
- Use exemplos da vida real, metáforas, momentos de superação e luz interior.
- Reflita o estilo visto no site dela: https://thaisgalassi.com.br

Final:
- Termine com um desfecho impactante, profundo e emocional, com frases que tocam o coração, como se fosse a última mensagem que ela deixaria para o ouvinte hoje.
- Use palavras com peso emocional e toques de hipnose positiva: acolhimento, fé, entrega, despertar, coragem, amor, perdão e luz.

Formato:
- Comece com o título do tema em negrito.
- Depois escreva "RESUMO" e o conteúdo de 16 linhas.
- Depois escreva "TEXTO COMPLETO" e o conteúdo de 100 linhas.
- Use espaçamento entre os parágrafos para facilitar a leitura.
- O texto deve fluir como uma conversa íntima, sem tópicos ou perguntas.

Data de referência para temas: {data_atual}
"""

# Formatação de texto com quebra de linhas
def formatar_linhas(texto, num_linhas):
    linhas = texto.strip().splitlines()
    linhas = [linha.strip() for linha in linhas if linha.strip()]
    return "\n\n".join(linhas[:num_linhas])

# Geração do conteúdo com DeepSeek
def gerar_conteudo():
    prompt = gerar_prompt(tema)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Você é um roteirista para podcasts emocionantes no estilo da Thais Galassi."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
    )

    conteudo = response.choices[0].message.content

    linhas = conteudo.strip().splitlines()
    if linhas:
        titulo = linhas[0].strip("**").strip()
        conteudo_sem_titulo = "\n".join(linhas[1:]).strip()
        partes = conteudo_sem_titulo.split("RESUMO")
        if len(partes) > 1:
            resumo_e_texto = partes[1].split("TEXTO COMPLETO")
            if len(resumo_e_texto) == 2:
                resumo = formatar_linhas(resumo_e_texto[0], 16)
                texto_completo = formatar_linhas(resumo_e_texto[1], 100)
                return f"## 🧠 **{titulo}**\n\n### RESUMO\n\n{resumo}\n\n---\n\n### TEXTO COMPLETO\n\n{texto_completo}"
    return conteudo

# Botões
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎧 Gerar conteúdo"):
        novo_conteudo = gerar_conteudo()
        if st.session_state.conteudo_atual:
            st.session_state.historico.insert(0, st.session_state.conteudo_atual)
        st.session_state.conteudo_atual = novo_conteudo

with col2:
    if st.button("🔄 Gerar outro conteúdo"):
        novo_conteudo = gerar_conteudo()
        if st.session_state.conteudo_atual:
            st.session_state.historico.insert(0, st.session_state.conteudo_atual)
        st.session_state.conteudo_atual = novo_conteudo

# Exibir conteúdo atual
if st.session_state.conteudo_atual:
    st.markdown("### 🎤 Conteúdo gerado:")
    st.markdown(st.session_state.conteudo_atual)

# Exibir histórico
if st.session_state.historico:
    st.markdown("---")
    st.markdown("### 📚 Conteúdos anteriores:")
    for item in st.session_state.historico:
        st.markdown(item)
        st.markdown("---")
