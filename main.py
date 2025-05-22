import streamlit as st
import requests

API_URL = "http://localhost:5001"

st.title("🔐 Chat Privado")
st.write("Simulação de conversa criptografada entre Usuário 1 e Usuário 2.")

# 🔹 Opção de escolha da criptografia
method = st.radio("Escolha o método de criptografia:", ("AES", "RSA"))

# Espaço para armazenar as mensagens separadamente
if "chat1_messages" not in st.session_state:
    st.session_state.chat1_messages = []

if "chat2_messages" not in st.session_state:
    st.session_state.chat2_messages = []

# 🔹 Função para truncar mensagens longas
def truncate_message(message, length=60):
    return message[:length] + "..." if len(message) > length else message

# 🔹 Chat do Usuário 1
st.write("📩 **Chat do Usuário 1**")
for message, message_type in st.session_state.chat1_messages:
    align = "margin-left: auto;" if message_type == "sent" else ""
    color = "#1976D2" if message_type == "sent" else "#388E3C"
    truncated_message = truncate_message(message)

    st.markdown(f'<div style="background-color: {color}; padding: 10px; border-radius: 10px; width: 60%; {align} margin-bottom: 5px; color: white;">{truncated_message}</div>', unsafe_allow_html=True)

    if len(message) > 60:
        with st.expander("Ver mensagem completa"):
            st.text(message)

# 🔹 Área de input e botão do Usuário 1
texto_usuario1 = st.text_area("Usuário 1: Digite sua mensagem")
if st.button("Enviar como Usuário 1"):
    if texto_usuario1:
        response = requests.post(f"{API_URL}/send_message", json={"message": texto_usuario1, "method": method})
        encrypted_message = response.json()["encrypted_message"]
        st.session_state.chat1_messages.append((encrypted_message, "sent"))

        response = requests.post(f"{API_URL}/receive_message", json={"encrypted_message": encrypted_message, "method": method})
        decrypted_message = response.json()["decrypted_message"]
        st.session_state.chat2_messages.append((decrypted_message, "received"))

        st.experimental_rerun()

# 🔹 Chat do Usuário 2
st.write("📨 **Chat do Usuário 2**")
for message, message_type in st.session_state.chat2_messages:
    align = "margin-left: auto;" if message_type == "sent" else ""
    color = "#1976D2" if message_type == "sent" else "#388E3C"
    truncated_message = truncate_message(message)

    st.markdown(f'<div style="background-color: {color}; padding: 10px; border-radius: 10px; width: 60%; {align} margin-bottom: 5px; color: white;">{truncated_message}</div>', unsafe_allow_html=True)

    if len(message) > 60:
        with st.expander("Ver mensagem completa"):
            st.text(message)

# 🔹 Área de input e botão do Usuário 2
texto_usuario2 = st.text_area("Usuário 2: Digite sua mensagem")
if st.button("Enviar como Usuário 2"):
    if texto_usuario2:
        response = requests.post(f"{API_URL}/send_message", json={"message": texto_usuario2, "method": method})
        encrypted_message = response.json()["encrypted_message"]
        st.session_state.chat2_messages.append((encrypted_message, "sent"))

        response = requests.post(f"{API_URL}/receive_message", json={"encrypted_message": encrypted_message, "method": method})
        decrypted_message = response.json()["decrypted_message"]
        st.session_state.chat1_messages.append((decrypted_message, "received"))

        st.experimental_rerun()
