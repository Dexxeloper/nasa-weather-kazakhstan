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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Аналитика",
    "🌱 Посадить или подождать",
    "🌡 Угадай температуру",
    "🌍 Мир и климат",
    "🎓 Обучение агрария",
    "🎮 Симуляция фермера"
])



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
    st.header("🌾 Agro Decision Challenge")

    # Выбор культуры
    crop_type = st.selectbox("🌱 Выберите культуру для посадки:", ["Пшеница", "Кукуруза", "Рис"])

    # Получаем случайную строку данных
    row = df.sample(1).iloc[0]
    date = pd.to_datetime(row["date"]).date()
    temp = row["temperature_C"]
    rain = row["precipitation_mm"]

    st.markdown(f"📅 **Дата:** {date} 🌡 **Температура:** {temp:.1f} °C 🌧 **Осадки:** {rain:.1f} мм")
    st.markdown("### Что вы решите сегодня?")

    col1, col2 = st.columns(2)
    with col1:
        plant = st.button("🌾 Посадить урожай", key="plant")
    with col2:
        wait = st.button("⏳ Подождать", key="wait")

    if plant or wait:
        st.session_state["rounds"] += 1

        # Логика исхода в зависимости от культуры
        outcome = "neutral"
        message = "🤔 Умеренные условия."

        if crop_type == "Пшеница":
            if 15 <= temp <= 25 and 1 <= rain <= 4:
                outcome = "good"
                message = "✅ Отличные условия для пшеницы!"
            elif temp > 30 and rain < 1:
                outcome = "bad"
                message = "🔥 Слишком жарко и сухо для пшеницы."
            elif temp < 10 and rain > 5:
                outcome = "bad"
                message = "❄️ Слишком холодно и влажно для пшеницы."

        elif crop_type == "Кукуруза":
            if 22 <= temp <= 30 and 2 <= rain <= 6:
                outcome = "good"
                message = "🌽 Идеально для кукурузы!"
            elif temp < 15:
                outcome = "bad"
                message = "🥶 Слишком холодно для кукурузы."
            elif rain > 8:
                outcome = "bad"
                message = "🌊 Залив — кукуруза не выживет."

        elif crop_type == "Рис":
            if 24 <= temp <= 32 and rain >= 5:
                outcome = "good"
                message = "🍚 Прекрасно для риса!"
            elif rain < 3:
                outcome = "bad"
                message = "💧 Недостаток влаги для риса."
            elif temp < 18:
                outcome = "bad"
                message = "❄️ Недостаточно тепла для риса."

        # ==== Оценка действий пользователя ====
        if plant:
            if outcome == "good":
                st.success(f"👍 Урожай '{crop_type}' будет отличным! {message}")
                st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTZtc3pwdGxuNnVyd2RreG0yMmlvbG1yaWE4aTZwbjc4dnVjaTg3YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ii7PnebaafSSlP6dFV/giphy.gif", caption="Рост 🌱")
                st.balloons()
                st.session_state["score"] += 1
            elif outcome == "bad":
                st.error(f"👎 Неудачный выбор для '{crop_type}'. {message}")
                st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExazJndXJib2s3d3ZtM2lkZ2psNGN4MjR6aTcxYmpzNGE2cXZydDlkciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZgUU4915HJ7snCN99b/giphy.gif", caption="Проблемы с урожаем ❌")
                st.session_state["fails"] += 1
            else:
                st.info(f"😐 Нейтрально. {message}")
                st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3psdHBvN2hpNG5iYjhpdG1iMzBsdHNieGR1ODk3eTZ6bnU3dThwZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kju8pHztX3hTw8uv5c/giphy.gif ", caption="Всё спокойно 🌥")

        else:  # wait
            if outcome == "bad":
                st.success(f"✅ Правильно подождали — условия плохие для '{crop_type}'.")
                st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTZtc3pwdGxuNnVyd2RreG0yMmlvbG1yaWE4aTZwbjc4dnVjaTg3YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ii7PnebaafSSlP6dFV/giphy.gif", caption="Фермер переждал ☁️")
                st.session_state["score"] += 1
            elif outcome == "good":
                st.warning(f"🙃 Вы упустили отличные условия для '{crop_type}'.")
                st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExazJndXJib2s3d3ZtM2lkZ2psNGN4MjR6aTcxYmpzNGE2cXZydDlkciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZgUU4915HJ7snCN99b/giphy.gif", caption="Жалко... 🌾")
                st.session_state["fails"] += 1
            else:
                st.info("🙂 Решение подождать — разумно в таких условиях.")
                st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3psdHBvN2hpNG5iYjhpdG1iMzBsdHNieGR1ODk3eTZ6bnU3dThwZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kju8pHztX3hTw8uv5c/giphy.gif", caption="Пока что всё тихо 🌤")

            st.markdown("---")
            st.subheader("📈 Ваша статистика:")

            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Успешные решения", st.session_state["score"])
            col2.metric("❌ Ошибки", st.session_state["fails"])
            col3.metric("🔁 Раунды", st.session_state["rounds"])

            if st.session_state["rounds"] > 0:
                success_rate = (st.session_state["score"] / st.session_state["rounds"]) * 100
                st.markdown(f"**🎯 Точность принятия решений:** {success_rate:.1f}%")
    

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

with tab4:
    import folium
    from streamlit_folium import st_folium

    st.header("🌍 Глобальные климатические тренды")
    st.markdown("Сравните погодные условия в Казахстане с другими странами мира.")

    # Пример координат и значений (можно заменить на реальные)
    climate_data = [
        {"name": "Казахстан", "lat": 48.0, "lon": 67.0, "temp": 25, "rain": 3},
        {"name": "США", "lat": 39.0, "lon": -98.0, "temp": 30, "rain": 2},
        {"name": "Бразилия", "lat": -10.0, "lon": -55.0, "temp": 28, "rain": 6},
        {"name": "Индия", "lat": 20.0, "lon": 78.0, "temp": 32, "rain": 8},
        {"name": "Кения", "lat": -1.0, "lon": 37.0, "temp": 27, "rain": 5},
    ]

    # Создаём карту
    world_map = folium.Map(location=[30, 0], zoom_start=2)

    for entry in climate_data:
        tooltip = f"{entry['name']}<br>🌡 {entry['temp']} °C<br>🌧 {entry['rain']} мм"
        folium.CircleMarker(
            location=[entry['lat'], entry['lon']],
            radius=10,
            popup=tooltip,
            color="blue" if entry['rain'] > 5 else "red",
            fill=True,
            fill_color="green" if entry['temp'] <= 28 else "orange",
            fill_opacity=0.7
        ).add_to(world_map)

    st_folium(world_map, width=700, height=450)

    # ===================== 🎓 ОБРАЗОВАТЕЛЬНЫЙ БЛОК =====================
with tab5:
    st.header("🎓 Образовательный блок: Как стать аграрием будущего")

    st.markdown("""
    Здесь вы узнаете, как принимать аграрные решения, используя реальные климатические данные от NASA.

    ---  
    ### 🛰 Какие данные мы используем?
    - **Температура (°C)** – влияет на выбор культур  
    - **Осадки (мм)** – определяют необходимость полива  
    - **Индекс NDVI** *(в будущем)* – здоровье растительности  
    - **Влажность почвы** *(данные SMAP)* – помогает планировать полив  

    ---  
    ### 🌾 Когда лучше сажать?
    - ✅ **Оптимум:** 20–28 °C, 1–5 мм осадков  
    - ⚠️ **Риск засухи:** >30 °C и <1 мм  
    - ⚠️ **Риск гниения:** <10 °C и >5 мм  

    ---
    ### 🚀 Что дальше?
    - Планируется добавление:
        - анализа почвы
        - солнечной радиации
        - индекса NDVI
        - симуляции роста культур

    """)

    st.success("✅ Используйте данные — и станьте цифровым фермером!")

    with st.expander("📚 Что такое NDVI?"):
        st.markdown("""
        **NDVI (Normalized Difference Vegetation Index)** — спутниковый индекс здоровья растительности.

        **Значения NDVI:**
        - 🌿 > 0.4 — здоровая растительность
        - 🏜 < 0.2 — пустыня или мёртвая зона
        - ❄️ < 0 — лёд или облака

        👉 Мы планируем подключить данные NDVI из NASA Earth Observations.
        """)
    # ===================== 🎮 СИМУЛЯЦИЯ ФЕРМЕРА =====================
with tab6:
    st.header("🎮 Симулятор фермера")
    st.markdown("Попробуйте вырастить урожай, используя реальные данные NASA!")

    crop_choice = st.selectbox("🌾 Выберите культуру:", ["Пшеница", "Кукуруза", "Рис"])

    random_row = df.sample(1).iloc[0]
    sim_temp = random_row["temperature_C"]
    sim_rain = random_row["precipitation_mm"]
    sim_date = pd.to_datetime(random_row["date"]).date()

    st.markdown(f"📅 **Дата:** {sim_date} — 🌡 {sim_temp:.1f} °C — 🌧 {sim_rain:.1f} мм")

    if st.button("🚜 Посадить культуру"):
        st.markdown("🧑‍🌾 Посадка культуры...")
        with st.spinner("⏳ Ждём погодных условий..."):
            import time
            time.sleep(2)

        if 20 <= sim_temp <= 28 and 1 <= sim_rain <= 5:
            st.success(f"✅ Урожай {crop_choice.lower()} взошёл успешно!")
            st.image("https://media.giphy.com/media/2kPjz3HM7npVy/giphy.gif", caption="Урожай растёт 🌱")
        elif sim_temp > 30 and sim_rain < 1:
            st.error(f"☀️ Слишком жарко. Урожай {crop_choice.lower()} не выжил.")
            st.image("https://media.giphy.com/media/CMczvTCZpsXJq/giphy.gif", caption="Засуха ❌")
        elif sim_temp < 10 and sim_rain > 5:
            st.error(f"❄️ Сырость и холод повредили {crop_choice.lower()}.")
            st.image("https://media.giphy.com/media/j6d5uE5N9bT1OBX1TE/giphy.gif", caption="Замерзшая ферма ❄️")
        else:
            st.warning("🤔 Урожай взошёл частично. Попробуйте снова.")
            st.image("https://media.giphy.com/media/gifXZrGSAkbM/giphy.gif", caption="Умеренные условия")


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


