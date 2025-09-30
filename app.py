import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NASA Weather Kazakhstan", page_icon="🌾", layout="centered")

# Заголовок
st.title("🌾 NASA Weather Kazakhstan")
st.markdown("""
Прогнозирование погодных условий для фермеров на основе данных NASA.  
Вы можете выбрать период и получить визуализацию температуры, осадков и рекомендации по посеву.
""")

# Загрузка данных
df = pd.read_csv("weather_kazakhstan.csv")
df['date'] = pd.to_datetime(df['date'])

# Блок выбора даты
st.sidebar.header("📅 Выбор диапазона дат")
start_date = st.sidebar.date_input("Начальная дата", df['date'].min().date())
end_date = st.sidebar.date_input("Конечная дата", df['date'].max().date())

# Фильтрация по дате
mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# Визуализация температуры
st.subheader("🌡 Температура воздуха (°C)")
fig1, ax1 = plt.subplots()
ax1.plot(filtered_df['date'], filtered_df['temperature_C'], color='darkorange')
ax1.set_ylabel("Температура (°C)")
ax1.set_xlabel("Дата")
st.pyplot(fig1)

# Визуализация осадков
st.subheader("🌧 Осадки (мм)")
fig2, ax2 = plt.subplots()
ax2.bar(filtered_df['date'], filtered_df['precipitation_mm'], color='skyblue')
ax2.set_ylabel("Осадки (мм)")
ax2.set_xlabel("Дата")
st.pyplot(fig2)

# AI-подсказка (простая логика)
st.subheader("📊 Рекомендации по погоде")

avg_temp = filtered_df['temperature_C'].mean()
avg_precip = filtered_df['precipitation_mm'].mean()

# Температурный анализ
if avg_temp > 30:
    st.warning("🔥 Высокая температура — возможна засуха. Рекомендуется отложить посев.")
elif avg_temp < 5:
    st.info("🥶 Слишком холодно для посева. Подождите потепления.")
else:
    st.success("✅ Температура благоприятна для посева.")

# Осадки
if avg_precip > 10:
    st.warning("☔️ Слишком много осадков — возможны переувлажнения.")
elif avg_precip < 1:
    st.warning("💧 Мало осадков — учитывайте полив.")
else:
    st.success("✅ Уровень осадков в норме.")

