import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NASA Weather Kazakhstan", page_icon="🌾", layout="centered")

# Заголовок
st.markdown("<h1 style='text-align: center; color: green;'>🌾 NASA Weather Kazakhstan</h1>", unsafe_allow_html=True)

st.markdown("""
<center>
Интеллектуальный погодный помощник для фермеров Казахстана.  
Данные NASA + локальные измерения = умные решения для посева 🌍  
</center>
""", unsafe_allow_html=True)

st.markdown("---")

with st.expander("ℹ️ О проекте"):
    st.markdown("""
    **Цель:** снизить риски фермеров, связанных с погодой  
    **Источники данных:** NASA POWER, локальные сенсоры  
    **Ключевые функции:**
    - Прогноз погоды
    - Умные рекомендации
    - Интерактивная карта
    """)


# Загрузка данных
df = pd.read_csv("weather_kazakhstan.csv")
df['date'] = pd.to_datetime(df['date'])

st.download_button(
    label="📥 Скачать CSV с погодными данными",
    data=df.to_csv(index=False),
    file_name='weather_kazakhstan.csv',
    mime='text/csv'
)


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

import folium
from streamlit_folium import st_folium

st.subheader("🗺 Погодная карта (экспериментальная версия)")

# Средняя точка для карты (Астана)
m = folium.Map(location=[51.1605, 71.4704], zoom_start=5)

# Добавим точки с температурой и осадками
for _, row in filtered_df.iterrows():
    tooltip = f"{row['date'].date()}<br>🌡 {row['temperature_C']}°C<br>🌧 {row['precipitation_mm']} мм"
    folium.Marker(
        location=[51.1605, 71.4704],  # пока одна локация (Астана)
        tooltip=tooltip,
        icon=folium.Icon(color='green', icon='cloud')
    ).add_to(m)

# Покажем карту
st_data = st_folium(m, width=700)


st.subheader("📊 Рекомендации по погоде")

# Расчёты
avg_temp = filtered_df['temperature_C'].mean()
max_temp = filtered_df['temperature_C'].max()

avg_precip = filtered_df['precipitation_mm'].mean()
max_precip = filtered_df['precipitation_mm'].max()

st.markdown(f"""
**Средняя температура:** {avg_temp:.1f} °C  
**Максимальная температура:** {max_temp:.1f} °C  
**Средние осадки:** {avg_precip:.1f} мм  
**Максимальные осадки:** {max_precip:.1f} мм
""")

# Условная "AI" логика
col1, col2 = st.columns(2)

with col1:
    st.metric("🌡 Средняя температура", f"{avg_temp:.1f} °C", delta=None)
    st.metric("🌡 Макс. температура", f"{max_temp:.1f} °C", delta=None)

with col2:
    st.metric("🌧 Средние осадки", f"{avg_precip:.1f} мм", delta=None)
    st.metric("🌧 Макс. осадки", f"{max_precip:.1f} мм", delta=None)

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



