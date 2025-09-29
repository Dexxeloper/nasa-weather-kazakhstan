import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Загружаем CSV
df = pd.read_csv("weather_kazakhstan.csv", parse_dates=['date'])
df.set_index('date', inplace=True)

# Классификация условий
def classify_conditions(temp, rain):
    if rain < 5:
        return "Засуха"
    elif rain > 20:
        return "Переувлажнение"
    elif temp < 5:
        return "Слишком холодно"
    else:
        return "Нормально"

def give_recommendation(condition):
    if condition == "Нормально":
        return "✅ Подходит для посадки"
    elif condition == "Засуха":
        return "⚠️ Риск засухи – подождите"
    elif condition == "Переувлажнение":
        return "⚠️ Переувлажнение – не рекомендуется"
    elif condition == "Слишком холодно":
        return "❄️ Слишком холодно – не сажать"
    else:
        return "Нет данных"

df['condition'] = df.apply(lambda row: classify_conditions(row['temperature_C'], row['precipitation_mm']), axis=1)
df['recommendation'] = df['condition'].apply(give_recommendation)

# Интерфейс Streamlit
st.title("🌾 Прогноз для фермера (на основе данных NASA)")
st.write("Выберите диапазон дат:")

date_range = st.date_input("Диапазон", [df.index.min().date(), df.index.max().date()])

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]

    st.subheader("📈 Температура воздуха")
    st.line_chart(filtered_df['temperature_C'])

    st.subheader("🌧️ Осадки")
    st.line_chart(filtered_df['precipitation_mm'])

    st.subheader("📋 Рекомендации по дням")
    st.dataframe(filtered_df[['temperature_C', 'precipitation_mm', 'condition', 'recommendation']])
