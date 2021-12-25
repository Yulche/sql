import sqlite3

connection = sqlite3.connect("works.sqlite")
cursor = connection.cursor()
cursor.execute('drop table if exists educations')
cursor.execute('create table educations ('
               'education text primary key)')
cursor.execute('insert into educations values("Высшее")')
cursor.execute('insert into educations values("Незаконченное высшее")')
cursor.execute('insert into educations values("Среднее")')
cursor.execute('insert into educations values("Среднее профессиональное")')
print(cursor.execute('select * from educations').fetchall())
