import streamlit as st
import requests

st.set_page_config(page_title="Support Routing AI", page_icon="🎧", layout="centered")

st.title("🎧 Умный маршрутизатор поддержки")
st.markdown("Эта ML-система автоматически определяет отдел для обращения на базе текста.")

# API URL (FastAPI)
API_URL = "http://127.0.0.1:8000/predict"

ticket_text = st.text_area("Введите текст обращения клиента:", height=150, placeholder="Например: I want a refund right now, the service is terrible!")

if st.button("Маршрутизировать тикет 🚀"):
    if ticket_text.strip():
        with st.spinner("Модель анализирует текст..."):
            try:
                response = requests.post(API_URL, json={"text": ticket_text})
                if response.status_code == 200:
                    data = response.json()
                    department = data["department"]
                    confidence = data["confidence"]
                    
                    st.success(f"**Определен отдел:** {department}")
                    st.info(f"**Уверенность сети:** {confidence * 100:.1f}%")
                else:
                    st.error(f"Ошибка API: {response.status_code}")
            except Exception as e:
                st.error(f"Не удалось подключиться к API. Сервер FastAPI запущен?\n{e}")
    else:
        st.warning("Пожалуйста, введите текст тикета.")
