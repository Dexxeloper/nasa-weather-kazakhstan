import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🌤 Weather Game Hub", layout="centered")

# 🎯 Состояние
if "score" not in st.session_state: st.session_state.score = 0
if "fails" not in st.session_state: st.session_state.fails = 0
if "rounds" not in st.session_state: st.session_state.rounds = 0
if "history" not in st.session_state: st.session_state.history = []

# 📊 Боковая панель
with st.sidebar:
    st.markdown("## 📊 Статистика")
    st.metric("Побед", st.session_state.score)
    st.metric("Ошибок", st.session_state.fails)
    st.metric("Раундов", st.session_state.rounds)
    if st.button("🔁 Сбросить"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()


# 📁 Данные
df = pd.read_csv("weather_kazakhstan.csv")
df["date"] = pd.to_datetime(df["date"])

# 🎮 Выбор режима
mode = st.radio("Выберите режим игры:", ["🌱 Посадить или подождать", "🌡 Угадай температуру"])

# ─────────────────────────────────────────────
# 🌱 РЕЖИМ 1: Посадить или подождать
# ─────────────────────────────────────────────
if mode == "🌱 Посадить или подождать":
    st.title("🌾 Weather Decision Challenge")
    random_row = df.sample(1).iloc[0]
    date = random_row["date"].date()
    temperature = random_row["temperature_C"]
    precipitation = random_row["precipitation_mm"]

    st.markdown(f"**📅 Дата:** {date}  \n🌡 Температура: {temperature:.1f} °C  \n🌧 Осадки: {precipitation:.1f} мм")

    # 📈 График 7 дней
    df_sorted = df.sort_values("date")
    idx = df_sorted[df_sorted["date"] == pd.Timestamp(date)].index[0]
    last_7_days = df_sorted.iloc[max(0, idx-6):idx+1]

    fig, ax1 = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=last_7_days, x="date", y="temperature_C", ax=ax1, color="red", label="Температура")
    ax1.set_ylabel("Температура (°C)", color="red")
    ax2 = ax1.twinx()
    sns.barplot(data=last_7_days, x="date", y="precipitation_mm", ax=ax2, alpha=0.3, color="blue")
    ax2.set_ylabel("Осадки (мм)", color="blue")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown("### 💭 Ваше действие:")
    col1, col2 = st.columns(2)
    with col1: plant = st.button("🌱 Посадить")
    with col2: wait = st.button("⏳ Подождать")

    with st.expander("ℹ️ Подсказка"):
        st.markdown("""
        - > 30°C и < 1 мм → засуха  
        - < 10°C и > 5 мм → холод и влажность  
        - 20–28°C и 1–5 мм → идеальные условия  
        - > 10 мм осадков → переувлажнение
        """)

    if plant or wait:
        st.session_state.rounds += 1
        if temperature > 30 and precipitation < 1:
            outcome = "bad"
            msg = "🔥 Слишком жарко и сухо — засуха."
        elif temperature < 10 and precipitation > 5:
            outcome = "bad"
            msg = "🌧 Холодно и сыро — риск загнивания."
        elif 20 <= temperature <= 28 and 1 <= precipitation <= 5:
            outcome = "good"
            msg = "✅ Отличные условия!"
        elif precipitation > 10:
            outcome = "bad"
            msg = "☔️ Слишком много осадков."
        else:
            outcome = "neutral"
            msg = "🙂 Умеренные условия."

        st.subheader("🔍 Результат:")
        st.markdown(msg)

        if plant:
            if outcome == "good":
                st.balloons()
                st.success("Урожай успешно посажен!")
                st.session_state.score += 1
            elif outcome == "bad":
                st.error("Урожай пострадал.")
                st.session_state.fails += 1
            else:
                st.info("Решение допустимо.")

        elif wait:
            if outcome == "good":
                st.warning("Вы могли посадить — условия были отличные.")
                st.session_state.fails += 1
            elif outcome == "bad":
                st.success("Вы избежали неудачи.")
                st.session_state.score += 1
            else:
                st.info("Ожидание — нормальное решение.")

        st.session_state.history.append({
            "Дата": str(date),
            "Темп": f"{temperature:.1f}°C",
            "Осадки": f"{precipitation:.1f} мм",
            "Действие": "Посадить" if plant else "Подождать",
            "Результат": outcome
        })

    if st.button("🔄 Следующий день"): st.rerun()

    if st.session_state.history:
        st.markdown("### 🧾 История")
        st.dataframe(pd.DataFrame(st.session_state.history[::-1]))

# ─────────────────────────────────────────────
# 🌡 РЕЖИМ 2: Угадай температуру
# ─────────────────────────────────────────────
elif mode == "🌡 Угадай температуру":
    st.title("🌡 Угадай температуру")

    row = df.sample(1).iloc[0]
    date = row["date"].date()
    temperature = row["temperature_C"]

    st.markdown(f"📅 **Дата:** {date}")
    guess = st.selectbox("Выбери диапазон температуры:", [
        "< 5°C", "5–15°C", "15–25°C", "25–35°C", "> 35°C"
    ])

    correct = (
        ("< 5°C" and temperature < 5) or
        ("5–15°C" and 5 <= temperature < 15) or
        ("15–25°C" and 15 <= temperature < 25) or
        ("25–35°C" and 25 <= temperature < 35) or
        ("> 35°C" and temperature >= 35)
    )

    if st.button("🎯 Проверить"):
        st.session_state.rounds += 1
        if (
            (guess == "< 5°C" and temperature < 5) or
            (guess == "5–15°C" and 5 <= temperature < 15) or
            (guess == "15–25°C" and 15 <= temperature < 25) or
            (guess == "25–35°C" and 25 <= temperature < 35) or
            (guess == "> 35°C" and temperature >= 35)
        ):
            st.success(f"✅ Верно! Температура была {temperature:.1f} °C")
            st.session_state.score += 1
        else:
            st.error(f"❌ Неверно. Температура была {temperature:.1f} °C")
            st.session_state.fails += 1

    if st.button("🔄 Новый раунд"): st.rerun()
