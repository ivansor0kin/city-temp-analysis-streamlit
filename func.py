import pandas as pd
import requests
from sklearn.linear_model import LinearRegression

# Маппинг месяцев на сезоны
month_to_season = {12: "winter", 1: "winter", 2: "winter",
                   3: "spring", 4: "spring", 5: "spring",
                   6: "summer", 7: "summer", 8: "summer",
                   9: "autumn", 10: "autumn", 11: "autumn"}

# Функция анализа данных для одного города
def analyze_city(df, city):
    city_data = df[df['city'] == city].copy()

    # Скользящее среднее, стандартное отклонение и аномалии
    city_data['moving_avg'] = city_data['temperature'].rolling(window=30).mean()
    city_data['std_dev'] = city_data['temperature'].rolling(window=30).std()
    upper_bound = city_data['temperature'] > city_data['moving_avg'] + 2 * city_data['std_dev']
    lower_bound = city_data['temperature'] < city_data['moving_avg'] - 2 * city_data['std_dev']
    city_data['anomaly'] = lower_bound | upper_bound
    anomalies = city_data[city_data['anomaly']]

    # Группировка по сезону для профиля
    seasonal_stats = city_data.groupby('season')['temperature'].agg(['mean', 'std']).reset_index()

    # Тренд (регрессия)
    city_data['timestamp_ordinal'] = city_data['timestamp'].map(pd.Timestamp.toordinal)
    X = city_data[['timestamp_ordinal']].dropna()
    y = city_data['temperature'].dropna()
    model = LinearRegression()
    model.fit(X, y)
    trend = 'positive' if model.coef_[0] > 0 else 'negative'

    # Средняя, min, max температуры
    avg_temp = city_data['temperature'].mean()
    min_temp = city_data['temperature'].min()
    max_temp = city_data['temperature'].max()

    # Возврат результатов
    return {
        'city': city,
        'average_temp': avg_temp,
        'min_temp': min_temp,
        'max_temp': max_temp,
        'seasonal_profile': seasonal_stats,
        'trend': trend,
        'anomalies': anomalies,
        'city_data': city_data
    }

def is_temperature_normal(city, current_temp, seasonal_profiles):
    current_month = pd.Timestamp.now().month
    current_season = month_to_season[current_month]
    profile = seasonal_profiles.get(city)
    if profile is None:
        return False, (None, None)
    season_data = profile[profile["season"] == current_season]
    if season_data.empty:
        return False, (None, None)
    mean_temp = season_data["mean"].values[0]
    std_temp = season_data["std"].values[0]
    lower_bound = mean_temp - 2 * std_temp
    upper_bound = mean_temp + 2 * std_temp
    return lower_bound <= current_temp <= upper_bound, (lower_bound, upper_bound)

def is_valid_api_key(api_key):
    test_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": "London", "appid": api_key, "units": "metric"}
    response = requests.get(test_url, params=params)
    if response.status_code == 200:
        return True, None
    else:
        return False, response.json()