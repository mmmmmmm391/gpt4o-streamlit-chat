import streamlit as st
import openai
import os

st.set_page_config(page_title="GPT-4o Multimodal", page_icon="🤖")

# Ввод API ключа
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("API_KEY not найден. Установи его как переменную окружения.")
    st.stop()
openai.api_key = api_key

# Состояние сообщений
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Ты мощный помощник, умеешь создавать текст, изображения и видео"}]

st.title("GPT-4o Multimodal Chat")

# Отображение истории чата
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Ввод текста
prompt = st.chat_input("Напиши запрос...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Думаю..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

# Генерация изображения
st.markdown("## Генерация изображения")
image_prompt = st.text_input("Опиши, что нарисовать (на английском)", key="img_input")
if st.button("Создать изображение"):
    if image_prompt:
        with st.spinner("Рисую..."):
            img_response = openai.Image.create(
                prompt=image_prompt,
                n=1,
                size="512x512"
            )
            st.image(img_response['data'][0]['url'], caption="Сгенерировано GPT")

# Заготовка под видео
st.markdown("## Видео (в разработке)")
st.warning("Функция генерации видео скоро будет добавлена. Пока можешь использовать D-ID, Kaiber или Sora, если есть доступ.")