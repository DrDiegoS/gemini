import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="Gemini Chat", page_icon="🤖", layout="centered")

st.title("💡 Gemini AI - App com Streamlit")

# Carregar API Key com segurança
API_KEY = "AIzaSyByH3z3NfQ-hvUHOCV84ad0_QDIvrEX97w"  # Ideal: usar st.secrets ou variáveis de ambiente

# Escolha do modelo
model = st.selectbox("Escolha o modelo:", ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"])

# Campo para prompt
prompt = st.text_area("Digite seu prompt:", "Explique como funciona a inteligência artificial em poucas palavras")

# Histórico de conversas
if "history" not in st.session_state:
    st.session_state.history = []

# Botão
if st.button("Gerar Resposta"):
    if not prompt.strip():
        st.error("Por favor, insira um prompt.")
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
                    st.session_state.history.append((prompt, output_text))
                    st.success(f"Resposta gerada em {elapsed} segundos.")
                    st.markdown(f"**Resposta:**\n\n{output_text}")
                    st.download_button("📥 Baixar resposta", output_text, file_name="resposta.txt")
                else:
                    st.warning("Nenhuma resposta gerada.")
            else:
                st.error(f"Erro {response.status_code}: {response.text}")

# Exibir histórico
if st.session_state.history:
    st.subheader("Histórico")
    for i, (q, a) in enumerate(reversed(st.session_state.history[-5:])):
        st.markdown(f"**Você:** {q}")
        st.markdown(f"**Gemini:** {a}")
        st.write("---")
