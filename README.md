# city-temp-analysis-with-Streamlit

## Анализ температурных данных и мониторинг текущей температуры

**Цель проекта:**  
Разработка решения для анализа исторических температурных данных и мониторинга текущей температуры в выбранных городах с использованием OpenWeatherMap API. Проект включает проведение анализа временных рядов, выявление аномалий, создание сезонных профилей и разработку интерактивного веб-приложения.

## Выполненные задачи

### 1. Анализ временных рядов исторических данных:
- Вычислено скользящее среднее с окном в 30 дней для сглаживания температурных колебаний.
- Рассчитаны средние значения температуры и стандартное отклонение для каждого сезона в каждом городе.
- Определены аномалии температуры, которые выходят за пределы диапазона:  
  $$ \text{скользящее среднее} \pm 2\sigma $$
- Построены долгосрочные тренды изменения температуры с использованием линейной регрессии.
- Исследована эффективность параллельной обработки данных:
  - Сравнена скорость выполнения анализа данных при последовательной и параллельной обработке с использованием `multiprocessing` и `concurrent.futures`.

### 2. Мониторинг текущей температуры через OpenWeatherMap API:
- Интеграция с OpenWeatherMap API для получения текущей температуры в выбранных городах.
- Реализована проверка, является ли текущая температура нормальной для текущего сезона на основе исторических данных.
- Сравнены подходы синхронного и асинхронного выполнения запросов к API для оптимизации времени отклика.

### 3. Разработка интерактивного веб-приложения:
- Реализовано приложение на Streamlit, предоставляющее пользователю следующие возможности:
  - Загрузка файла с историческими данными в формате CSV.
  - Выбор города из выпадающего списка для анализа.
  - Отображение описательной статистики по историческим данным, включая средние, минимальные и максимальные значения температуры.
  - Построение временного ряда с выделением аномалий (точками другого цвета).
  - Визуализация сезонных профилей с указанием среднего значения и стандартного отклонения.
- Подключена форма для ввода API-ключа OpenWeatherMap. Реализована проверка валидности ключа с выводом сообщений об ошибках в формате JSON.
- Реализован вывод текущей температуры и её сравнение с историческим нормальным диапазоном.

## Используемые данные
Исторические данные о температуре содержались в файле `temperature_data.csv`, включающем следующие столбцы:
- `city`: Название города.
- `timestamp`: Дата в формате `YYYY-MM-DD`.
- `temperature`: Среднесуточная температура (в °C).
- `season`: Сезон года (зима, весна, лето, осень).

## Технологии и инструменты
- **Язык программирования:** Python
- **Библиотеки:** Pandas, NumPy, Matplotlib, Plotly, Streamlit, aiohttp, requests, scikit-learn
- **Параллельная обработка:** `multiprocessing`, `concurrent.futures`
- **API:** OpenWeatherMap
- **Деплой:** Streamlit Cloud

## Результаты
- Проанализированы исторические данные о температуре для выявления аномалий и сезонных закономерностей.
- Разработано интерактивное веб-приложение для визуализации данных и мониторинга текущей температуры.
- Проведён сравнительный анализ подходов синхронного и асинхронного выполнения запросов, выбраны оптимальные решения.
- Решение успешно развернуто на платформе Streamlit Cloud. 
