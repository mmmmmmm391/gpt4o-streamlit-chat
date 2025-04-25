import streamlit as st
import openai
import os

st.set_page_config(page_title="GPT-4o Chat", page_icon=":robot_face:")
st.title("GPT-4o Chatbot")

api_key = os.getenv("API_KEY")
if not api_key:
    st.error("API_KEY not found in environment variables.")
    st.stop()

openai.api_key = api_key

# Инициализация сообщений
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Вывод истории сообщений
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Ввод нового сообщения
prompt = st.chat_input("Say something...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            stream=False
        )
        answer = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
