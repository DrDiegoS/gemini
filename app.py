import streamlit as st
import requests
import json
import time
import os  # Para acessar variáveis de ambiente
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

st.set_page_config(page_title="Gemini Chat", page_icon="🤖", layout="wide")  # 'wide' para tela cheia

# ---- Sidebar ----
with st.sidebar:
    st.title("🤖 Gemini AI Chat")
    st.markdown("Um chatbot com a API Gemini.")
    st.markdown("---")
    # API Key (usando st.secrets para maior segurança)
    API_KEY = st.text_input("Chave da API Google Gemini", type="password", value=os.getenv("GOOGLE_API_KEY", ""))  # Pega do .env ou deixa em branco
    if not API_KEY:
        st.warning("Por favor, insira sua chave da API Google Gemini.")
    st.markdown("---")
    st.markdown(
        """
        **Informações:**
        *  Utiliza a API Google Gemini (Generative AI).
        *  [Documentação da API](https://ai.google.dev/)
        *  [Como obter uma chave API](https://makersuite.google.com/app/apikey)
        """
    )

# ---- Main Area ----

# Escolha do modelo
model = st.selectbox("Escolha o modelo:", ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"])

# Histórico de conversas (mais visual)
if "history" not in st.session_state:
    st.session_state.history = []

def display_conversation():
    """Exibe o histórico de conversas em caixas separadas."""
    for i, (q, a) in enumerate(reversed(st.session_state.history)):
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            st.markdown(a)


# Input Area (na parte inferior para dar a aparência de chat)
prompt = st.chat_input("Digite sua pergunta:") # Usando st.chat_input

if prompt:
    # Adiciona a pergunta ao histórico imediatamente
    st.session_state.history.append((prompt, ""))
    display_conversation() # Atualiza a tela para mostrar a pergunta do usuário

    if not API_KEY:
        st.error("Por favor, insira sua chave da API Google Gemini na barra lateral.")
    else:
        with st.spinner("Gerando resposta..."):
            start_time = time.time()
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            headers = {"Content-Type": "application/json", "X-goog-api-key": API_KEY}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            elapsed = round(time.time() - start_time, 2)

            if response.status_code == 200:
                data = response.json()
                if "candidates" in data:
                    output_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    # Atualiza o histórico com a resposta do modelo
                    st.session_state.history[-1] = (prompt, output_text) # Substitui o "" pela resposta
                    # Mostra a resposta
                    with st.chat_message("assistant"):
                        st.markdown(output_text)
                    st.success(f"Resposta gerada em {elapsed} segundos.")
                    st.download_button("📥 Baixar resposta", output_text, file_name="resposta.txt")
                else:
                    st.warning("Nenhuma resposta gerada.")
            else:
                st.error(f"Erro {response.status_code}: {response.text}")

# Exibe o histórico de conversas (após a geração da resposta)
display_conversation()
