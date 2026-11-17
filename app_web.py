"""Chatbot com interface web (Streamlit).

Rode com:  streamlit run app_web.py
"""

import streamlit as st

from src.chatbot import create_chat
from src.config import APP_TITLE

st.set_page_config(page_title=APP_TITLE, page_icon="🤖")
st.title(f"🤖 {APP_TITLE}")
st.caption("Tire dúvidas de Cisco, redes, Python e Linux.")


def nova_conversa() -> None:
    """Zera o histórico e cria um novo chat."""
    st.session_state.messages = []
    st.session_state.chat = create_chat()


# O Streamlit roda o script inteiro a cada interação, então tudo que precisa
# "sobreviver" (histórico e objeto do chat) fica no session_state.
if "chat" not in st.session_state:
    try:
        nova_conversa()
    except RuntimeError as erro:
        st.error(str(erro))
        st.stop()

with st.sidebar:
    st.header("Opções")
    if st.button("🗑️ Nova conversa"):
        nova_conversa()
        st.rerun()

# Mostra o histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caixa de entrada
if prompt := st.chat_input("Pergunte algo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        espaco = st.empty()
        texto = ""
        try:
            for pedaco in st.session_state.chat.send_message_stream(prompt):
                texto += pedaco.text or ""
                espaco.markdown(texto + "▌")
            espaco.markdown(texto)
        except Exception as erro:
            texto = f"⚠️ Erro ao falar com a API: {erro}"
            espaco.error(texto)

    st.session_state.messages.append({"role": "assistant", "content": texto})
