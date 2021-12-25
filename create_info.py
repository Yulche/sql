import pandas as pd
import nltk
import sqlite3
import re
import pymystem3
from tqdm import tqdm

stemmer = nltk.stem.snowball.SnowballStemmer("russian")
m = pymystem3.Mystem()


def items_stem_top(name, items, word_filter, stem_filter, top, fast=True):
    items_dict = {}

    for item in tqdm([i for i in items]):
        tokens = [wordpunkt for wordpunkts in [nltk.wordpunct_tokenize(word) for word in nltk.word_tokenize(item)] for
                  wordpunkt in wordpunkts if len(wordpunkt) > 3] if fast else m.analyze(item)
        for token in [t for t in tokens if word_filter(t)]:
            stem_token = stemmer.stem(token) if fast else token['analysis'][0]['lex']
            if not stem_filter(stem_token):
                continue
            if stem_token not in items_dict:
                items_dict[stem_token] = [0, set()]
            items_dict[stem_token][0] += 1
            items_dict[stem_token][1].add(token if fast else token['text'])

    top_items_list = [item for item in sorted(items_dict.items(), key=lambda i: i[1][0], reverse=True)][:top]
    return pd.DataFrame({f'{name}': [item[0] for item in top_items_list],
                         'count': [item[1][0] for item in top_items_list],
                         'words': [', '.join(item[1][1]) for item in top_items_list]})


def add_to_db(series, name, db_connection):
    cursor = db_connection.cursor()
    cursor.execute(f'drop table if exists {name}s')
    cursor.execute(f'create table {name}s ('
                   f'{name} text primary key)')
    series.to_sql(f'{name}s', db_connection, if_exists="append", index=False)


works = pd.read_csv('init_works.csv')

connection = sqlite3.connect("works.sqlite")

jt_qlf_endings = ['ер', 'ир', 'ор', 'ар', 'ец', 'ик', 'ел', 'ист', 'ант', 'ог', 'ож', 'ач', 'ед', 'иц']
jt_qlf_errors = ['начальник', 'руководител', 'заместител', 'завед', 'помощник', 'специалист', 'мастер', 'консультант',
                 'технолог', 'работник', 'представител', 'делопроизводител', 'отдел', 'товар', 'свер', 'дел', 'категор',
                 'издел', 'прибор', 'втор', 'кред', 'территор', 'сектор', 'сотрудник', 'командир', 'ученик',
                 'организатор', 'стажер', 'мебел', 'практикант', 'выдач', 'сист', 'педагогик', 'автоматик', 'сфер',
                 'границ', 'компенсир']

attribute = 'jobTitle'
add_to_db(items_stem_top(attribute, works[attribute].dropna(),
                         lambda word: True,
                         lambda stem: any([stem.endswith(end) for end in jt_qlf_endings]) and stem not in jt_qlf_errors,
                         100)[attribute], attribute, connection)

attribute = 'qualification'
add_to_db(items_stem_top(attribute, works[attribute].dropna(),
                         lambda word: True,
                         lambda stem: any([stem.endswith(end) for end in jt_qlf_endings]) and stem not in jt_qlf_errors,
                         100)[attribute], attribute, connection)


def clear_from_html(s):
    return re.sub(r'\<[^>]*\>', '', s)


skills_errors = ['nbsp', 'быстр', 'профессиональн', 'больш', 'легк', 'высок', 'laquo', 'сво', 'raquo', 'офисн', 'нов',
                 'хорош', 'общ', 'различн', 'повышен', 'bull', 'электрон', 'люб', 'sbquo', 'отличн', 'дан', 'правов',
                 'нормативн', 'письмен', 'рабоч', 'бол', 'ndash', 'друг', 'mdash', 'кассов', 'первичн', 'трудов',
                 'разн', 'Power', 'Point', 'прав', 'основн', 'государствен', 'индивидуальн', 'постоя', 'собствен',
                 'кадров']


def skills_word_filter(word):
    tag = nltk.pos_tag([word], lang='rus')[0][1]
    return tag.startswith('A') or tag == 'NONLEX'


attribute = 'skills'
add_to_db(items_stem_top(attribute, [clear_from_html(skill) for skill in works.skills.dropna()],
                         skills_word_filter,
                         lambda s: s not in skills_errors, 58)[attribute], attribute, connection)

otherInfo_errors = ['вредный', 'личный', 'новый', 'высокий', 'электронный', 'большой', 'научный', 'государственный',
                    'различный', 'международный', 'общий', 'детский', 'студенческий', 'рабочий', 'трудовой',
                    'дополнительный', 'полный', 'собственный', 'российский', 'разный', 'базовый', 'настоящий',
                    'производственный', 'последний', 'удаленный', 'внутренний', 'заочный', 'социальный', 'московский',
                    'всероссийский', 'горный', 'региональный', 'учебный', 'огромный', 'кадровый', 'частный', 'средний',
                    'основной', 'единый', 'муниципальный', 'общественный', 'необходимый', 'начальный', 'официальный',
                    'длительный', 'индивидуальный']

attribute = 'otherInfo'
add_to_db(items_stem_top(attribute, [clear_from_html(info) for info in works.otherInfo.dropna()],
                         lambda w: 'analysis' in w and len(w['analysis']) > 0 and w['analysis'][0]['gr'].startswith(
                             'A='),
                         lambda s: s not in otherInfo_errors, 54, False)[attribute], attribute, connection)
