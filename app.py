import streamlit as st
import requests
import json

# Configurações da página
st.set_page_config(page_title="Gemini App", page_icon="🤖", layout="centered")

st.title("💡 Gemini AI - App com Streamlit")
st.write("Este app consome a API do Gemini (Google AI) para gerar conteúdo com IA.")

# Campo para API Key (não armazenamos isso, apenas sessão)
api_key = st.text_input("Insira sua API Key do Google AI", type="password")

# Campo para prompt do usuário
prompt = st.text_area("Digite seu prompt:", "Explique como funciona a inteligência artificial em poucas palavras")

# Botão para gerar resposta
if st.button("Gerar Resposta"):
    if not api_key:
        st.error("Por favor, insira a sua API Key.")
    else:
        # Endpoint do Gemini
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        # Cabeçalhos
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }

        # Payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                data = response.json()
                # Acessando a resposta gerada
                if "candidates" in data and len(data["candidates"]) > 0:
                    output_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    st.subheader("Resposta do Gemini:")
                    st.write(output_text)
                else:
                    st.warning("Nenhuma resposta gerada. Verifique o prompt.")
            else:
                st.error(f"Erro {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
