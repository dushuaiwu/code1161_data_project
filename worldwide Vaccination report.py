import xlrd
import matplotlib
from collections import Counter
from pyecharts.charts import Pie
from matplotlib import pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Map
import pyecharts.options as opts
from pyecharts.charts import Line


# Only seleted 10 countries among huge datas
data = xlrd.open_workbook('./data.xlsx')
table = data.sheets()[0]
nrows = table.nrows  # hang
ncols = table.ncols  # lie
all_data = []


# open all datas
for i in range(0, nrows):
    data = []
    rowValues = table.row_values(i)
    for item in rowValues:
        data.append(item)
    all_data.append(data)


country = []

country_name = []

population = []

infections_number = []

death_number = []

total_vaccinations = []

people_fully_vaccinated = []
# different vaccines
vaccine = []

for i in range(len(all_data)):

    country_n = all_data[i][5]
    country.append(country_n)

    name = all_data[i][4]
    country_name.append(name)

    popu = all_data[i][0]
    population.append(popu)

    infect = all_data[i][2]
    infections_number.append(infect)

    death = all_data[i][3]
    death_number.append(death)

    vaccinations = all_data[i][7]
    total_vaccinations.append(vaccinations)

    fully_vaccinated = all_data[i][9]
    people_fully_vaccinated.append(fully_vaccinated)

    vac = all_data[i][14]
    vaccine.append(vac)

country = country[1:]
population = population[1:]
infections_number = infections_number[1:]
death_number = death_number[1:]
total_vaccinations = total_vaccinations[1:]
people_fully_vaccinated = people_fully_vaccinated[1:]
vaccine = vaccine[1:]
country_name = country_name[1:]
print(country)
print(population)
print(infections_number)
print(death_number)
print(total_vaccinations)
print(people_fully_vaccinated)
print(vaccine)

# avoid err
plt.rcParams['font.sans-serif'] = ['SimHei']

# Population ratio map of each country
pie = (
    Pie()
    .add(
        "",
        [(i, j)for i, j in zip(country_name, population)],
        radius=["30%", "75%"],
        center=["25%", "50%"],
        rosetype="radius",
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title=" "))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)
pie.render_notebook()


# Vaccination rates in each countries
Vaccination_rate = []
for i in range(len(country)):
    rate = float('{:.2}'.format(total_vaccinations[i]/population[i]))
    Vaccination_rate.append(rate)
print(Vaccination_rate)
plt.bar(country, Vaccination_rate)
plt.title('Vaccination rates in each countries')
plt.show()

# The Fully vaccination rate in each country
fully_Vaccination_rate = []
for i in range(len(country)):
    rate = float('{:.2}'.format(people_fully_vaccinated[i]/population[i]))
    fully_Vaccination_rate.append(rate)
plt.pie(fully_Vaccination_rate, labels=country,
        wedgeprops=dict(width=0.3, edgecolor='w'))
plt.axis('equal')
plt.show()

# Full coverage rate of vaccinated people
fully_Vaccination_rate2 = []
for i in range(len(country)):
    rate = float('{:.2}'.format(
        people_fully_vaccinated[i]/total_vaccinations[i]))
    fully_Vaccination_rate2.append(rate)
print(fully_Vaccination_rate2)
plt.title('fully_Vaccination_reta')
plt.plot(country, fully_Vaccination_rate2, 's-',
         color='r', label="ATT-RLSTM")  # s-:方形
plt.show()

# covid_19 Infection rate
infections_rate = []
for i in range(len(country)):
    rate = float('{:.2}'.format(infections_number[i]/population[i]))
    infections_rate.append(rate)
print(infections_rate)
matplotlib.rc('font', family='SimHei', weight='bold')
plt.barh(range(len(infections_rate)), infections_rate, tick_label=country)
plt.title('covid_19 Infection rate')
plt.show()

# covid_19 death rate
death_rate = []
for i in range(len(country)):
    rate = float('{:.2}'.format(death_number[i]/infections_number[i]))
    death_rate.append(rate)
plt.plot(country, death_rate, 'bo', ms=5)
plt.title('covid_19 death rate')
plt.show()

# different vaccines
vaccine_type = []
for va in vaccine:
    if '/' in va:
        va = str(va)
        type = va.split('/')
        for i in type:
            vaccine_type.append(i)
    else:
        vaccine_type.append(va)
# counter
vaccine_type_number = dict(Counter(vaccine_type))

vaccine_name = list(vaccine_type_number)
vaccine_number = list(vaccine_type_number.values())
patches, text1, text2 = plt.pie(vaccine_number,
                                labels=vaccine_name,
                                labeldistance=1.2,
                                autopct='%3.2f%%',
                                shadow=False,
                                startangle=90,
                                pctdistance=0.6)
plt.axis('equal')
plt.legend()
plt.show()


data = []
for index in range(len(country)):
    city_ionfo = [country_name[index], death_number[index]]
    data.append(city_ionfo)
c = (
    Map()
    .add("death", data, "world")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="covid_19 worldwide death number"),
        visualmap_opts=opts.VisualMapOpts(max_=200),

    )
)
c.render_notebook()


country_names = ['China', 'Australia', 'USA', 'Indonesia']
data_number = ['2020/12/1', '2021/1/1', '2021/2/1', '2021/3/1',
               '2021/4/1', '2021/5/1', '2021/6/1', '2021/7/1', '2021/8/1', ]
China_number = [1500000, 4500000, 31200000, 52520000,
                126616000, 270406000, 681908000, 1264149000, 1669527000]
Australia_number = [0, 0, 20, 33702, 744328,
                    2234844, 4362739, 7970153, 12317727]
USA_number = [556208, 4225756, 32222402, 76899987,
              153631404, 243463471, 296404240, 328152304, 346456669]
Indonesia_number = [0, 132000, 574938, 3023348,
                    12226028, 20172516, 27308881, 44160960, 68151247]
line = (
    Line()
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    .add_xaxis(xaxis_data=data_number)
    .add_yaxis(
        series_name="China",
        y_axis=China_number,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_xaxis(xaxis_data=data_number)
    .add_yaxis(
        series_name="Australia",
        y_axis=Australia_number,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_xaxis(xaxis_data=data_number)
    .add_yaxis(
        series_name="USA",
        y_axis=USA_number,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .add_xaxis(xaxis_data=data_number)
    .add_yaxis(
        series_name="Indonesia",
        y_axis=Indonesia_number,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
    )
)

line.render_notebook()
