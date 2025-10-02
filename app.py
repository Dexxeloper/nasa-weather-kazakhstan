import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

# — Настройка страницы —
st.set_page_config(
    page_title="🌾 Агро-Погода Казахстана",
    layout="centered",
    page_icon="🌤️",
)

st.title("🌾 Агро-Погода Казахстана")
st.markdown("Погодный помощник для фермеров, аграриев и исследователей.")
st.markdown("""
Приложение анализирует метеоданные NASA по Казахстану и помогает:
- 📊 Понимать погодные тренды
- 🌱 Делать правильный выбор для посадки
- 💡 Получать рекомендации на основе данных
""")
st.markdown("---")

# Настройки страницы
st.set_page_config(page_title="🌤 NASA Weather Kazakhstan", layout="centered")
st.markdown("<style>h1, h2 { color: #1f77b4; }</style>", unsafe_allow_html=True)

# Инициализация состояния
for key in ["score", "fails", "rounds", "history"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key != "history" else []

# Загружаем CSV
df = pd.read_csv("weather_kazakhstan_with_region.csv")
df["date"] = pd.to_datetime(df["date"])

# Выбор региона (если колонка есть)
if "region" in df.columns:
    selected_region = st.selectbox("🌍 Выберите регион:", sorted(df["region"].unique()))
    df = df[df["region"] == selected_region]
else:
    st.warning("📌 В данных нет информации о регионах. Показываем общий анализ.")

# Обновлённый диапазон дат после фильтрации по региону
date_min = df["date"].min().date()
date_max = df["date"].max().date()

import random

regions = ['Астана', 'Алматы', 'Шымкент']
df['region'] = [random.choice(regions) for _ in range(len(df))]

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Аналитика", "🌱 Посадить или подождать", "🌡 Угадай температуру"])

# ===================== 📊 АНАЛИТИКА =====================
with tab1:
    st.header("Анализ погодных условий")
    with st.expander("📆 Как выбрать дату?"):
        st.info("Выберите период анализа. Например, неделю перед посадкой.")
date_range = st.date_input(
    "📆 Выберите диапазон дат:",
    [date_min, date_max],
    min_value=date_min,
    max_value=date_max,
    key="date_range_selector"
)


if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
else:
    st.warning("Пожалуйста, выберите начальную и конечную дату.")
    st.stop()


filtered_df = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)]

st.line_chart(filtered_df.set_index("date")[["temperature_C", "precipitation_mm"]])

st.subheader("📊 Рекомендации по погоде")

avg_temp = filtered_df["temperature_C"].mean()
avg_precip = filtered_df["precipitation_mm"].mean()

st.markdown(f"""
- **Средняя температура:** {avg_temp:.1f} °C  
- **Средние осадки:** {avg_precip:.1f} мм
""")

if avg_temp > 30 and avg_precip < 1:
    st.error("🔥 Жарко и сухо — риск засухи!")
elif avg_temp < 10 and avg_precip > 5:
    st.warning("🌧 Холодно и влажно — осторожно с посадкой.")
elif 20 <= avg_temp <= 28 and 1 <= avg_precip <= 5:
    st.success("✅ Отличные условия для посева!")
else:
    st.info("🤔 Условия умеренные.")

# ===================== 🌱 ИГРА №1 =====================
with tab2:
    st.header("🌾 Weather Decision Challenge")

row = df.sample(1).iloc[0]
date = pd.to_datetime(row["date"]).date()
temp = row["temperature_C"]
rain = row["precipitation_mm"]

st.markdown(f"📅 **Дата:** {date} 🌡 **Температура:** {temp:.1f} °C 🌧 **Осадки:** {rain:.1f} мм")

st.markdown("### Что вы решите сегодня?")
col1, col2 = st.columns(2)
with col1:
    plant = st.button("🌱 Посадить урожай", key="plant")
with col2:
    wait = st.button("⏳ Подождать", key="wait")

if plant or wait:
    st.session_state["rounds"] += 1

    if temp > 30 and rain < 1:
        outcome = "bad"
        message = "🔥 Засуха. Урожай пострадал."
    elif temp < 10 and rain > 5:
        outcome = "bad"
        message = "🌧 Сырость и холод. Урожай загнил."
    elif 20 <= temp <= 28 and 1 <= rain <= 5:
        outcome = "good"
        message = "✅ Отличные условия для роста!"
    elif rain > 10:
        outcome = "bad"
        message = "☔️ Слишком много дождя."
    else:
        outcome = "neutral"
        message = "🤔 Условия умеренные."

    if plant:
        if outcome == "good":
            st.success("👍 Отличный выбор! " + message)
            st.session_state["score"] += 1
        elif outcome == "bad":
            st.error("👎 Ошибка. " + message)
            st.session_state["fails"] += 1
        else:
            st.info("😐 Нейтральный исход. " + message)
    else:  # wait
        if outcome == "bad":
            st.success("✅ Вы избежали плохих условий.")
            st.session_state["score"] += 1
        elif outcome == "good":
            st.warning("🙃 Упустили шанс на хороший урожай.")
            st.session_state["fails"] += 1
        else:
            st.info("🙂 Ожидание — нормальный выбор.")

# ===================== 🌡 ИГРА №2 =====================
with tab3:
    st.header("🌡 Угадай температуру")

row = df.sample(1).iloc[0]
date = pd.to_datetime(row["date"]).date()
true_temp = row["temperature_C"]
rain = row["precipitation_mm"]

st.markdown(f"📅 **Дата:** {date} 🌧 **Осадки:** {rain:.1f} мм")

guess = st.slider("Угадайте температуру (°C):", -40, 50, 20)

if st.button("Проверить", key="check_temp"):
    st.session_state["rounds"] += 1
    diff = abs(true_temp - guess)
    if diff <= 2:
        st.balloons()
        st.success(f"🎯 Почти идеально! Было {true_temp:.1f} °C.")
        st.session_state["score"] += 1
    elif diff <= 5:
        st.info(f"🙂 Неплохо. Было {true_temp:.1f} °C.")
    else:
        st.error(f"😕 Ошибка. На самом деле: {true_temp:.1f} °C.")
        st.session_state["fails"] += 1
if avg_temp > 30 and avg_precip < 1:
    st.error("🔥 Очень жарко и сухо — высокая вероятность засухи. Подумайте об устойчивых культурах.")
elif avg_temp > 25 and avg_precip < 3:
    st.warning("💨 Тёплая и сухая погода — возможен дефицит влаги. Рекомендуется капельный полив.")
elif avg_temp < 10 and avg_precip > 5:
    st.warning("🌧 Холодно и влажно — риск загнивания. Рекомендуется отсрочка посадки.")
elif avg_precip > 10:
    st.warning("☔️ Много осадков — возможна переувлажнённость почвы.")
else:
    st.success("✅ Погодные условия благоприятны для посева.")

st.markdown("---")
st.markdown("<center><small>Разработано на хакатоне. Автор: @Dexxeloper • 2025</small></center>", unsafe_allow_html=True)

st.markdown("---")
with st.expander("ℹ️ О проекте"):
    st.markdown("""
    **Проект:** NASA Weather Kazakhstan  
    **Автор:** Dexxeloper (AGROKAZAKH )  
    **Источник данных:** NASA POWER (https://power.larc.nasa.gov)  
    **Используемые технологии:** Streamlit, Pandas, Folium, Matplotlib  
    **Цель:** Сделать агро-аналитику доступной каждому фермеру.

    🌐 GitHub: [Перейти](https://github.com/Dexxeloper/nasa-weather-kazakhstan)  
    📊 Онлайн: [Streamlit App](https://nasa-weather-kazakhstan-n7oskv2uzq3ipbpskj2tzb.streamlit.app/)
    """)


