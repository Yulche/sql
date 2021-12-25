import sqlite3
import pandas as pd

connection = sqlite3.connect("works.sqlite")
cursor = connection.cursor()
cursor.execute('drop table if exists works')
cursor.execute('create table works ('
               'ID integer primary key AUTOINCREMENT,'
               'salary integer,'
               'educationType text,'
               'jobTitle text,'
               'qualification text,'
               'gender text,'
               'dateModify text,'
               'skills text,'
               'otherInfo text,'
               'FOREIGN KEY(gender) REFERENCES genders(gender),'
               'FOREIGN KEY(educationType) REFERENCES educations(education),'
               'FOREIGN KEY(jobTitle) REFERENCES jobTitles(jobTitle),'
               'FOREIGN KEY(qualification) REFERENCES qualifications(qualification))')
df = pd.read_csv("mod_works.csv")
df.to_sql("works", connection, if_exists="append", index=False)
