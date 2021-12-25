import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

connection = sqlite3.connect("works.sqlite")
cursor = connection.cursor()

# 1. Выведите количество записей.

print(cursor.execute('select count(*) from works').fetchone()[0])  # 32683

# 2. Выведите количество мужчин и женщин.

print(cursor.execute('select count(*) from works where gender = "Мужской"').fetchone()[0])  # 13386
print(cursor.execute('select count(*) from works where gender = "Женский"').fetchone()[0])  # 17910

# 3. У скольки записей заполнены skills?

print(cursor.execute('select count(*) from works where skills != "None"').fetchone()[0])  # 8972

# 4. Получить заполненные скиллы.

print(cursor.execute('select skills from works where skills != "None"').fetchone())

# 5. Вывести зарплату только у тех, у кого в скиллах есть Python.

print(cursor.execute('select count(*) from works where skills like "%Python%"').fetchone()[0])

# 6. Построить перцентили и разброс по з/п у мужчин и женщин.

print(pd.read_sql('select salary from works where gender = "Мужской"', connection).describe()[3:].transpose())
print(pd.read_sql('select salary from works where gender = "Женский"', connection).describe()[3:].transpose())

# 7. Построить графики распределения по з/п мужчин и женщин (а также в зависимости от высшего образования).

for (gender, ed) in [(gender, ed)
                     for ed in ("Высшее", "Незаконченное высшее", "Среднее", "Среднее профессиональное")
                     for gender in ('Мужской', 'Женский')]:
    sql_query = f'select salary from works where gender = "{gender}" and educationType = "{ed}"'
    salary = [row[0] for row in cursor.execute(sql_query).fetchall()]
    plt.hist(salary, bins=100)
    plt.title(f'{gender} заработок с образованием "{ed}"')
    plt.show()
