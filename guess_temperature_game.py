import streamlit as st
import pandas as pd
import random
st.set_page_config(page_title="🌡 Угадай температуру", page_icon="🌤", layout="centered")

st.title("🌡 Игра: Угадай температуру")
st.markdown("Попробуй угадать температуру по дате и осадкам!")

# Загружаем данные
df = pd.read_csv("weather_kazakhstan.csv")

# Сохраняем состояние между раундами
if "score" not in st.session_state:
    st.session_state.score = 0
if "rounds" not in st.session_state:
    st.session_state.rounds = 0

# Выбираем случайную строку
random_row = df.sample(1).iloc[0]
date = pd.to_datetime(random_row["date"]).date()
precip = random_row["precipitation_mm"]
true_temp = random_row["temperature_C"]

st.markdown(f"""
📅 **Дата:** {date}  
🌧 **Осадки:** {precip:.1f} мм
""")

# Варианты ответа
guess = st.radio(
    "Какой была температура?",
    ["< 10°C", "10–25°C", "> 25°C"]
)

if st.button("Проверить ответ"):
    st.session_state.rounds += 1

    # Проверяем
    if true_temp < 10:
        correct = "< 10°C"
    elif true_temp > 25:
        correct = "> 25°C"
    else:
        correct = "10–25°C"

    if guess == correct:
        st.success(f"✅ Верно! Температура была {true_temp:.1f}°C")
        st.session_state.score += 1
    else:
        st.error(f"❌ Неверно. Температура была {true_temp:.1f}°C")

    st.markdown(f"**Очки:** {st.session_state.score} / {st.session_state.rounds}")

    if st.button("🔁 Следующий вопрос"):
        st.rerun()
