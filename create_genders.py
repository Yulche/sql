import sqlite3

connection = sqlite3.connect("works.sqlite")
cursor = connection.cursor()
cursor.execute('drop table if exists genders')
cursor.execute('create table genders ('
               'gender text primary key)')
cursor.execute('insert into genders values("Мужской")')
cursor.execute('insert into genders values("Женский")')
print(cursor.execute('select * from genders').fetchall())
