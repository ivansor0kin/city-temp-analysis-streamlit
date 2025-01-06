import streamlit as st
import pandas as pd
import requests
from func import analyze_city, is_temperature_normal, is_valid_api_key
import plotly.graph_objects as go

st.title("Анализ температурных данных")

# Описание структуры файла
st.markdown("""
#### Требования к структуре загружаемого файла
- Файл должен быть в формате **CSV**.
- Должны присутствовать следующие столбцы:
  - **city**: Название города (строка).
  - **timestamp**: Дата в формате `YYYY-MM-DD`.
  - **temperature**: Среднесуточная температура (число).
  - **season**: Сезон года (строка, например, "winter", "spring", "summer", "autumn").
""")

# Пример данных
example_data = pd.DataFrame({
    "city": ["New York", "New York", "New York", "New York", "New York"],
    "timestamp": ["2010-01-01", "2010-01-02", "2010-01-03", "2010-01-04", "2010-01-05"],
    "temperature": [-2.52, -0.34, -0.80, -1.99, 3.14],
    "season": ["winter", "winter", "winter", "winter", "winter"]
})

st.write("#### Пример данных:")
st.dataframe(example_data)

# Загрузка файла
st.write("#### Загрузите файл с историческими данными:")
uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=["timestamp"])
    st.write("#### Загруженные данные:")
    st.write(df.head())

if uploaded_file is not None:
    # Выбор города
    st.write("#### Выберите город:")
    city = st.selectbox("", df["city"].unique(), label_visibility="collapsed")
    analysis = analyze_city(df, city)

    # Описательная статистика
    st.write("#### Основные статистики:")
    st.metric("Средняя температура:", f"{analysis['average_temp']:.2f} °C")
    st.metric("Минимальная температура:", f"{analysis['min_temp']:.2f} °C")
    st.metric("Максимальная температура:", f"{analysis['max_temp']:.2f} °C")

    # Временной ряд с аномалиями
    st.write(f"#### Временной ряд температуры для города {city}:")
    city_data = analysis['city_data']

    # Настройка графика
    show_anomalies = st.checkbox("Показать аномалии", value=True)

    fig = go.Figure()

    # Линия температуры
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data['temperature'],
        mode='lines',
        name='Температура',
        line=dict(color='blue'),
    ))

    # Линия скользящего среднего
    fig.add_trace(go.Scatter(
        x=city_data['timestamp'],
        y=city_data['moving_avg'],
        mode='lines',
        name='Скользящее среднее',
        line=dict(color='red', dash='dash'),
    ))

    # Точки аномалий
    if show_anomalies and not analysis['anomalies'].empty:
        anomalies = analysis['anomalies']
        fig.add_trace(go.Scatter(
            x=anomalies['timestamp'],
            y=anomalies['temperature'],
            mode='markers',
            name='Аномалии',
            marker=dict(color='orange', size=6, symbol='x'),
        ))

    fig.update_layout(
        title=f"Температура и аномалии в городе {city}",
        xaxis_title="Дата",
        yaxis_title="Температура (°C)",
        legend_title="Легенда",
    )

    st.plotly_chart(fig)

    # Сезонный профиль
    st.write("#### Сезонный профиль:")
    st.dataframe(analysis['seasonal_profile'])

# Ввод API-ключа и проверка
st.write("#### Введите ваш OpenWeatherMap API Key:")
API_KEY = st.text_input("", type="password", label_visibility="collapsed")

# Проверка API-ключа
if API_KEY:

    is_valid, error_message = is_valid_api_key(API_KEY)
    if is_valid:
        st.session_state["api_key_validated"] = True
        st.success("API-ключ валиден!")
    else:
        st.session_state["api_key_validated"] = False
        st.error(f"Ошибка проверки API-ключа: {error_message}")

    # Если ключ валиден, показываем поле для выбора города
    if st.session_state.get("api_key_validated"):
        st.write("#### Введите города для получения текущей температуры:")
        city_for_temp = st.text_input(
            "",
            value=city if uploaded_file else "", label_visibility="collapsed"
        )

        if st.button("Получить текущую температуру"):
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city_for_temp,
                "appid": API_KEY,
                "units": "metric"
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]

                st.write(f"#### {city_for_temp}:")
                st.metric(f"Текущая температура:", f"{temp}°C ({description})")

                # Проверка на аномальность
                if uploaded_file is not None:
                    seasonal_profiles = {}
                    for city_name in df["city"].unique():
                        result = analyze_city(df, city_name)
                        seasonal_profiles[city_name] = result["seasonal_profile"]

                    is_normal, bounds = is_temperature_normal(city_for_temp, temp, seasonal_profiles)
                    if bounds[0] is not None:
                        st.metric("Нормальный диапазон температуры:", f"{bounds[0]:.2f}°C — {bounds[1]:.2f}°C")
                    if is_normal:
                        st.success("Температура в норме для текущего сезона.")
                    else:
                        st.warning("Температура аномальная для текущего сезона.")
            else:
                st.error("Ошибка получения данных. Проверьте название города.")