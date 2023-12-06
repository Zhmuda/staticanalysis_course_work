import pandas as pd
from scipy.stats import shapiro
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import scipy.stats
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
import statsmodels.api as sm


#'Потреб. Расходы': [27586, 28477, 29610, 31277, 41364, 31957],

# Создаем DataFrame
data_table1 = {
    'Годы': [2015, 2016, 2017, 2018, 2019, 2020],
    'Потреб. Расходы (тыс.)': [27586, 28477, 29610, 31277, 41364, 31957],

    'Абсолютные приросты (цепные)': [None, 891.10, 1133.18, 1666.76, 10087.49, -9407.45],
    'Абсолютные приросты (базисные)': [None, 891.10, 2024.28, 3691.04, 13778.53, 4371.08],


    'Темпы роста (цепные)': [None, 103.23, 103.98, 105.63, 132.25, 77.26],
    'Темпы роста (базисные)': [None, 103.23, 107.34, 113.38, 149.95, 115.85],

    'Темпы прироста (цепные)': [None, 3.23, 3.98, 5.63, 32.25, -22.74],
    'Темпы прироста (базисные)': [None, 3.23, 7.34, 13.38, 49.95, 15.85],

    'Абсолютные значение прироста': [None, 284.77, 296.11, 312.77, 413.65, 319.57]
}

df = pd.DataFrame(data_table1)

# Разбиваем DataFrame на списки
years = df['Годы'].tolist()
expenses = df['Потреб. Расходы (тыс.)'].tolist()

absolute_growth_chain = df['Абсолютные приросты (цепные)'].tolist()
absolute_growth_base = df['Абсолютные приросты (базисные)'].tolist()

growth_rates_chain = df['Темпы роста (цепные)'].tolist()
growth_rates_base = df['Темпы роста (базисные)'].tolist()


increment_rates_chain = df['Темпы прироста (цепные)'].tolist()
increment_rates_base = df['Темпы прироста (базисные)'].tolist()

absolute_values = df['Абсолютные значение прироста'].tolist()


# Проверка на нормальность с использованием теста Шапиро-Уилка
stat_shapiro, p_shapiro = shapiro(data_table1['Потреб. Расходы (тыс.)'])
print(f'Shapiro-Wilk Test: Statistic={stat_shapiro}, p-value={p_shapiro}')


years = data_table1['Годы']
consumer_spending = data_table1['Потреб. Расходы (тыс.)']
df = pd.DataFrame({'Consumer Spending': consumer_spending}, index=pd.to_datetime(years, format='%Y'))
df.index.freq = 'AS'

model = ExponentialSmoothing(df['Consumer Spending'], trend='add', seasonal=None, initialization_method="estimated")
result = model.fit()

forecast_years = range(2021, 2025)
forecast = result.predict(start=len(df), end=len(df) + len(forecast_years) - 1)

plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Consumer Spending'], marker='o', linestyle='-', color='b', label='Исходные данные')
plt.plot(pd.to_datetime(forecast_years, format='%Y'), forecast, marker='o', linestyle='--', color='r', label='Модель Хольта')
plt.title('Динамика и прогноз потребительских расходов населения 2015-2024 г.')
plt.xlabel('Годы')
plt.ylabel('Потреб. Расходы')
plt.legend()
plt.grid(True)
plt.show()


# Реализация метода Хольта
def holt_forecast(y, alpha, beta, n_forecast):
    m = len(y)
    level = y[0]
    trend = (y[m-1] - y[0]) / (m-1)

    forecasts = np.zeros(m + n_forecast)

    for i in range(m):
        forecasts[i] = level + i * trend

    for i in range(m, m + n_forecast):
        level = alpha * y[i-m] + (1 - alpha) * (level + trend)
        trend = beta * (level - y[i-m]) + (1 - beta) * trend
        forecasts[i] = level + i * trend

    return forecasts

data_table2 = {
    'Год': ['2015', '2016', '2017', '2018', '2019', '2020'],
    'На покупку продуктов для домашнего питания': [6951.75, 8258.45, 7728.36, 7662.95, 8686.62, 10058.58],
    'На питание вне дома': [1627.59, 1623.21, 1243.64, 1751.53, 2026.88, 910.79],
    'На покупку алкогольных напитков': [551.73, 626.50, 503.38, 594.27, 744.57, 894.81],
    'На покупку непродовольственных товаров': [9793.14, 10081.00, 11400.08, 11197.29, 15966.83, 9275.63],
    'На оплату услуг': [8662.10, 7888.24, 8735.12, 10071.30, 13939.95, 10817.57],
    'Итого': [27586.30, 28477.40, 29610.58, 31277.34, 41364.83, 31957.38],
    'Абсолютное Изменение': [3106.84, -716.81, 343.08, -517.51, 2155.47, 4371.08],
    'Темп роста %': [144.69, 55.96, 162.18, 94.72, 124.88, 115.85]
}

# Создание DataFrame
df2 = pd.DataFrame(data_table2)

# Выбор категорий для отображения на графике
categories = ['На покупку продуктов для домашнего питания', 'На питание вне дома', 'На покупку алкогольных напитков', 'На покупку непродовольственных товаров', 'На оплату услуг']

# Построение графика
plt.figure(figsize=(10, 8))

for category in categories:
    plt.plot(data_table2['Год'], data_table2[category], marker='o', label=category)

plt.title('Динамика Потребительских Расходов (2015-2020)')
plt.xlabel('Год')
plt.ylabel('Сумма расходов (руб.)')
plt.legend()
plt.grid(True)
plt.show()


# Параметры сглаживания
alpha = 0.5
beta = 0.2

# Количество точек для прогноза
n_forecast = 4

# Создаем график
plt.figure(figsize=(14, 10))

# Задаем цвета
colors = ['blue', 'orange', 'green', 'red', 'purple']

for i, category in enumerate(categories):
    # Прогноз для каждой категории
    data_category = data_table2[category]
    forecast = holt_forecast(data_category, alpha, beta, n_forecast)

    # Выводим результаты на график
    plt.plot(data_table2['Год'], data_category, label=f'Фактические данные: {category}', color=colors[i])
    plt.plot(np.arange(len(data_category), len(data_category) + n_forecast), forecast[-n_forecast:], linestyle='dashed', marker='o', label=f'Прогноз: {category}', color=colors[i])

plt.title('Прогноз потребительских расходов по категориям')
plt.xlabel('Год')
plt.ylabel('Сумма расходов (руб.)')
plt.legend()
plt.grid(True)
plt.show()


# Коэффициент Пирсона для зависимости потребления и покупку непрод товаров
potreb_rasxody = data_table1['Потреб. Расходы (тыс.)']
na_neprod_tovar = data_table2['На покупку непродовольственных товаров']

# Вычисляем средние значения переменных
mean_potreb_rasxody = sum(potreb_rasxody) / len(potreb_rasxody)
mean_na_neprod_tovar = sum(na_neprod_tovar) / len(na_neprod_tovar)

# Вычисляем ковариацию
covariance = sum((potreb_rasxody[i] - mean_potreb_rasxody) * (na_neprod_tovar[i] - mean_na_neprod_tovar) for i in range(len(potreb_rasxody)))

# Вычисляем стандартные отклонения
std_dev_potreb_rasxody = (sum((potreb_rasxody[i] - mean_potreb_rasxody) ** 2 for i in range(len(potreb_rasxody)))) ** 0.5
std_dev_na_neprod_tovar = (sum((na_neprod_tovar[i] - mean_na_neprod_tovar) ** 2 for i in range(len(na_neprod_tovar)))) ** 0.5

# Вычисляем коэффициент корреляции Пирсона
correlation_coefficient = covariance / (std_dev_potreb_rasxody * std_dev_na_neprod_tovar)

print(f"Коэффициент корреляции Пирсона: {correlation_coefficient}")
# Количество наблюдений
n = len(potreb_rasxody)

# Степени свободы
df = n - 2

# Вычисляем статистику t
t_statistic = correlation_coefficient * ((n - 2) ** 0.5) / ((1 - correlation_coefficient ** 2) ** 0.5)

# Вычисляем P-значение
p_value = 2 * (1 - abs(scipy.stats.t.cdf(t_statistic, df=df)))

# Вывод результатов
print(f"P-значение: {p_value}")


# Добавляем константу для расчета коэффициента сдвига (intercept)
potreb_rasxody_with_const = sm.add_constant(potreb_rasxody)

na_oplatu_uslug = data_table2['На оплату услуг']

# Строим регрессионную модель
model = sm.OLS(na_oplatu_uslug, potreb_rasxody_with_const)
result = model.fit()

print(result.summary())


df_na_food = pd.DataFrame(data_table2['На покупку продуктов для домашнего питания'], columns=['На покупку продуктов для домашнего питания'])
df_na_alcho = pd.DataFrame(data_table2['На покупку алкогольных напитков'], columns=['На покупку алкогольных напитков'])
df_potreb_rasxody_with_const = pd.DataFrame(potreb_rasxody_with_const, columns=['const', 'Потреб. Расходы (тыс.)'])

# Объединяем данные в один DataFrame
df_combined = pd.concat([df_na_food, df_na_alcho, df_potreb_rasxody_with_const], axis=1)

# Рассчитываем VIF для каждого предиктора
vif_combined = pd.DataFrame()
vif_combined["Variable"] = df_combined.columns
vif_combined["VIF"] = [variance_inflation_factor(df_combined.values, i) for i in range(df_combined.shape[1])]

print(vif_combined)


# Абсолютный прирост показателя потребительских расходов в 2020 году по сравнению с 2015 годом
abs_growth_2015_to_2020 = data_table1['Абсолютные приросты (базисные)'][5]
print(f"Абсолютный прирост 2015-2020: {abs_growth_2015_to_2020}")

# Темп роста в 2020 году по сравнению с 2015 годом
growth_rate_2015_to_2020 = data_table1['Темпы роста (базисные)'][5]
print(f"Темп роста 2015-2020: {growth_rate_2015_to_2020}")

# Темп прироста в 2020 году по сравнению с 2015 годом
growth_rate_2015_to_2020_absolute = data_table1['Темпы прироста (базисные)'][5]
print(f"Темп прироста 2015-2020: {growth_rate_2015_to_2020_absolute}")


# Наибольший объем потребительских расходов зафиксирован в 2019 году
max_spending_index = data_table1['Потреб. Расходы (тыс.)'].index(max(data_table1['Потреб. Расходы (тыс.)']))
max_spending_year = data_table1['Годы'][max_spending_index]
max_spending_value = max(data_table1['Потреб. Расходы (тыс.)'])
print(f"Наибольший объем потребительских расходов: {max_spending_value} руб. в {max_spending_year} году")


# Темп прироста показателя в 2019 году
growth_rate_2019 = data_table1['Темпы прироста (базисные)'][4]
print(f"Темп прироста потребительских расходов в 2019 году: {growth_rate_2019} %")


# Темп роста с 2015 по 2018 год
growth_rate_2015_to_2018 = data_table1['Темпы роста (базисные)'][3]
print(f"Темп роста потребительских расходов с 2015 по 2018 год: {growth_rate_2015_to_2018} %")


# Расходы на покупку продуктов для домашнего питания
abs_change_na_food = data_table2['Абсолютное Изменение'][0]
growth_rate_na_food = data_table2['Темп роста %'][0]
print(f"Абсолютное изменение расходов на покупку продуктов для домашнего питания: {abs_change_na_food} руб.")
print(f"Темп роста расходов на покупку продуктов для домашнего питания: {growth_rate_na_food} %")

# Расходы на питание вне дома
abs_change_na_out_food = data_table2['Абсолютное Изменение'][1]
# Покупка продуктов для домашнего питания
max_value_na_out_food = max(data_table2['На питание вне дома'])
peak_years_na_out_food = [year for year, value in zip(data_table2['Год'], data_table2['На питание вне дома']) if value == max_value_na_out_food]
peak_year_na_out_food = ', '.join(map(str, peak_years_na_out_food))
print(f"Пик расходов на питание вне дома зафиксирован в {peak_year_na_out_food} году: {max_value_na_out_food} руб.")


# Покупка непродовольственных товаров
max_value_na_non_food = max(data_table2['На покупку непродовольственных товаров'])
peak_years_na_non_food = [year for year, value in zip(data_table2['Год'], data_table2['На покупку непродовольственных товаров']) if value == max_value_na_non_food]
peak_year_na_non_food = ', '.join(map(str, peak_years_na_non_food))
print(f"Максимальные расходы на покупку непродовольственных товаров зафиксированы в {peak_year_na_non_food} году: {max_value_na_non_food} руб.")

