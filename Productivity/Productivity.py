#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import matplotlib.pyplot as plt
import matplotlib_style
matplotlib_style.set_style()

# Отчёт
import reportlab
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak
import reportlab_style
from reportlab_style import get_image
from reportlab.lib.units import cm

import datetime


df = pd.read_csv("Input/Kiln_Feed_Hour_Big.txt", sep=',', index_col=0, names=['date', 'value', 'code'],
                 parse_dates=True)
df.dropna(inplace=True)


# Производительность за всё время
df.value.plot()
plt.title('Производительность за всё время')
plt.xlabel('Время')
plt.ylabel('Производительность')
plt.savefig("Image/Производительность за всё время.png")
#plt.show()
plt.close()


# Кол-во часов работы с заданной производительностью
grouped = df.groupby(df.value)
len_by_value = grouped.size()
len_by_value.drop(0.0, inplace=True)
len_by_value.plot()
plt.title("Кол-во часов работы с заданной производительностью")
plt.xlabel("Производительность")
plt.ylabel("Кол-во часов работы")
plt.savefig("Image/Кол-во часов работы с заданной производительностью.png")
#plt.show()
plt.close()


# Средняя производительность в зависимости от времени суток
grouped = df.groupby(lambda x: x.hour)
mean_by_hourly = grouped.mean()
mean_by_hourly.value.plot(drawstyle='steps-pre', xticks=range(0, 25, 2))
plt.title("Средняя производительность по часам")
plt.xlabel("Часы")
plt.ylabel("Средняя производительность, т/ч")
plt.savefig("Image/Средняя производительность по часам.png")
#plt.show()
plt.close()


# Средняя производительность по дням недели
grouped = df.groupby(lambda x: x.isoweekday())
mean_by_weekday = grouped.mean()
mean_by_weekday.value.plot(drawstyle='steps-mid')
plt.title("Средняя производительность по дням недели")
plt.xlabel("День недели")
plt.ylabel("Средняя производительность, т/ч")
plt.savefig("Image/Средняя производительность по дням недели.png")
#plt.show()
plt.close()


# Производительность день / ночь
def func_day_or_night(day):
    if 8 < day.hour <= 20:
        return 'day'
    else:
        return 'night'
grouped = df.groupby(func_day_or_night)
day_or_night = grouped.mean()


# Производство по месяцам
def func_by_month(day):
    return datetime.datetime(day.year, day.month, 1)


def sum_zero(array):
    zero = 0
    for value in array:
        if value < 1:
            zero += 1
    return zero


def zero_percent(array):
    zero = sum_zero(array)
    return 100 * zero / len(array)

grouped = df.groupby(func_by_month)
monthly_stat = grouped.value.agg([np.sum, np.mean, sum_zero, zero_percent])
monthly_stat['mean'].plot(drawstyle='steps-mid')
plt.title("Средняя часовая производительность по месяцам")
plt.xlabel("Месяцы")
plt.ylabel("Средняя производительность, т/ч")
plt.savefig("Image/Средняя часовая производительность по месяцам.png")
#plt.show()
plt.close()

monthly_stat['zero_percent'].plot(drawstyle='steps-mid')
plt.title("Процент времени простоя по месяцам")
plt.xlabel("Месяцы")
plt.ylabel("Время простоя, %")
#plt.show()
plt.savefig("Image/Процент времени простоя по месяцам.png")
plt.close()


# Создаём отчёт -------------------
reportlab_style.add_russian_fonts()

styles = getSampleStyleSheet()
styles['Normal'].fontName = 'Droid Serif'
styles['Normal'].fontSize = 10
styles['Normal'].leading = 14
styles['Normal'].spaceBefore = 0.1 * cm
styles['Title'].fontName = 'Droid Serif'
styles['Title'].fontSize = 12

space_1cm = Spacer(1 * cm, 1 * cm)
image_width = 15 * cm

story = []

text = "Питание печи <br/> с {} по {}".format(df.index[0], df.index[-1])
story.append(Paragraph(text, styles['Title']))

text = "Подсчитано {} значений часовой производительности.".format(len(df))
story.append(Paragraph(text, styles['Normal']))

text = """За это время подано сырья на печь {:.3f} тыс. тонн;
в среднем за день {:.3f} тонн;
в среднем за час {:.3f} тонн.
""".format(df.value.sum(), 24 * df.value.mean(), df.value.mean())
story.append(Paragraph(text, styles['Normal']))

text = """Средняя производительность за дневную смену: {:.3f} т/ч,
за ночную: {:.3f} т/ч.""".format(day_or_night.value['day'], day_or_night.value['night'])
story.append(Paragraph(text, styles['Normal']))

text = "Максимальная производительность была {} и равна {} т/ч.".format(df.value.idxmax(), df.value.max())
story.append(Paragraph(text, styles['Normal']))

text = """Наибольшая производительность по времени суток - {:.3f} т/ч в промежуток времени {} - {} часов;
наименьшая - {:.3f} т/ч в промежуток времени {} - {} часов.
""".format(mean_by_hourly.value.max(), (mean_by_hourly.value.idxmax() - 1) % 24, mean_by_hourly.value.idxmax(),
           mean_by_hourly.value.min(), (mean_by_hourly.value.idxmin() - 1) % 24, mean_by_hourly.value.idxmin())
story.append(Paragraph(text, styles['Normal']))

text = """Наибольшая производительность по дням недели - {:.3f} т/ч в {} день недели;
наименьшая - {:.3f} т/ч в {} день недели.
""".format(mean_by_weekday.value.max(), mean_by_weekday.value.idxmax(),
           mean_by_weekday.value.min(), mean_by_weekday.value.idxmin())
story.append(Paragraph(text, styles['Normal']))

stop_percentage = 100 * df.value[df.value < 1].count() / df.value.count()
text = """За заданное время завод стоял {} часов, что составляет {:.3f} % времени.
Из каждого часа завод стоит {:.3f} минут.
""".format(df.value[df.value < 1].count(), stop_percentage, 60 * stop_percentage / 100)
story.append(Paragraph(text, styles['Normal']))


story.append(PageBreak())
story.append(get_image("Image/Производительность за всё время.png", image_width))
story.append(get_image("Image/Кол-во часов работы с заданной производительностью.png", image_width))
story.append(get_image("Image/Средняя производительность по часам.png", image_width))
story.append(get_image("Image/Средняя производительность по дням недели.png", image_width))
story.append(get_image("Image/Средняя часовая производительность по месяцам.png", image_width))
story.append(get_image("Image/Процент времени простоя по месяцам.png", image_width))

doc = SimpleDocTemplate("Output/Report.pdf")
doc.build(story)
