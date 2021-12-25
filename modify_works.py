import pandas as pd
import nltk
import sqlite3
import pymystem3
from tqdm import tqdm

m = pymystem3.Mystem()
stemmer = nltk.stem.snowball.SnowballStemmer("russian")
connection = sqlite3.connect("works.sqlite")
cursor = connection.cursor()
jobTitles = [row[0] for row in cursor.execute('select * from jobTitles')]
qualifications = [row[0] for row in cursor.execute('select * from qualifications')]
skills = [row[0] for row in cursor.execute('select * from skillss')]
otherInfo = [row[0] for row in cursor.execute('select * from otherInfos')]
init_works = pd.read_csv('init_works.csv')


def get_tag(attribute, attributes_list):
    if attribute != 'nan':
        tokens = [stemmer.stem(wordpunkt) for wordpunkts in
                  [nltk.wordpunct_tokenize(word) for word in nltk.word_tokenize(attribute)] for
                  wordpunkt in wordpunkts]
        for elem in attributes_list:
            if elem in tokens:
                return elem
    return None


def get_tags(attribute, attributes_list, fast=True):
    tags = set()
    if attribute != 'nan':
        tokens = [stemmer.stem(wordpunkt) for wordpunkts in
                  [nltk.wordpunct_tokenize(word) for word in nltk.word_tokenize(attribute)] for
                  wordpunkt in wordpunkts] if fast else m.lemmatize(attribute)
        for elem in tokens:
            if elem in attributes_list:
                tags.add(elem)
    return None if len(tags) == 0 else ', '.join(tags)


mod_works = pd.DataFrame(
    {'salary': init_works.salary, 'educationType': init_works.educationType,
     'jobTitle': [get_tag(str(item), jobTitles) for item in init_works.jobTitle],
     'qualification': [get_tag(str(item), qualifications) for item in init_works.qualification],
     'gender': init_works.gender, 'dateModify': init_works.dateModify,
     'skills': [get_tags(str(item), skills) for item in init_works.skills],
     'otherInfo': [get_tags(str(item), otherInfo, False) for item in tqdm(init_works.otherInfo)]})
mod_works.to_csv('mod_works.csv', encoding='utf-8', index=False)
