# -*- coding: utf-8 -*-
"""Clean take for model."""
import json
import re
import sys
import os

from sqlalchemy import create_engine
import pandas as pd
import nltk
from nltk.corpus import stopwords
import spacy

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

if os.name == 'nt':
    nlpname1 = 'Lib\\site-packages\\en_core_web_sm\\'
    nlpname2 = os.path.join(os.path.dirname(sys.executable), nlpname1)
    model = max([i for i in os.listdir(nlpname2) if re.fullmatch(
                r'(?:en_core_web_sm-\d{1,2}[\.]\d{1,2}[\.]\d{1,2})', i)])
    nlpname = os.path.join(nlpname2, model)
else:
    nlpname = 'en_core_web_sm'

spacy_nlp = spacy.load(nlpname)


def read_df():
    """Read df of brand name and puc from factotum."""
    with open('mysql.json', 'r') as f:
        cfg = json.load(f)['mysql']
    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           convert_unicode=True, echo=False)
    sqq = 'SELECT puc_id, product_id, brand_name, title, gen_cat, ' + \
          'prod_fam, prod_type, description ' + \
          'FROM ( SELECT brand_name, title, puc_id, product_id ' + \
          'FROM (select id, brand_name, ' + \
          'title from dashboard_product) as product ' + \
          'INNER JOIN (select puc_id, product_id ' + \
          'from dashboard_producttopuc) as prod_to_puc ' + \
          'ON product.id = prod_to_puc.product_id ) as product_match ' + \
          'INNER JOIN (select * from dashboard_puc) as puc ' + \
          'ON product_match.puc_id = puc.id;'
    df = pd.read_sql(sqq, engine)
    return df


# name processing
def clean(brand, title):
    """Cleanup name."""
    # words to exclude
    exclude = ['count', 'percent', 'inc', 'llc', 'ltd', 'co']

    # remove umlauts
    char = {"ä": "a", "ö": "o", "ü": "u", "Ä": "A", "Ö": "O", "Ü": "U"}
    for key, val in char.items():
        if key in brand:
            brand = brand.replace(key, val)
        if key in title:
            title = title.replace(key, val)

    # remove posessives
    brand = re.sub(r'([\w]+)[\'][s]\b', r'\g<1>', brand)
    title = re.sub(r'([\w]+)[\'][s]\b', r'\g<1>', title)

    # remove numbers
    brand = re.sub(r'[\<\>\s]?\d{1,}[.]?\d{0,}[\s\%]?(?:fl)?\s?(?:oz)?' +
                   r'(?:lb[s]?)?\s?(?:mm)?\s?(?:g)?\s?(?:ml)?\s?(?:ct)?' +
                   r'\s?(?:pc)?\s?',
                   ' ', brand)
    title = re.sub(r'[\<\>\s]?\d{1,}[.]?\d{0,}[\s\%]?(?:fl)?\s?(?:oz)?' +
                   r'(?:lb[s]?)?\s?(?:mm)?\s?(?:g)?\s?(?:ml)?\s?(?:ct)?' +
                   r'\s?(?:pc)?\s?',
                   ' ', title)

    # taking regex stuff from here
    # https://stackabuse.com/text-classification-with-python-and-scikit-learn/
    brand = brand.replace('-', '')
    title = title.replace('-', '')
    brand = re.sub(r'[\W_]', ' ', brand)
    title = re.sub(r'[\W_]', ' ', title)
    brand = re.sub(r'\s+[a-zA-Z]\s+', ' ', brand)
    title = re.sub(r'\s+[a-zA-Z]\s+', ' ', title)
    brand = re.sub(r'^[a-zA-Z]\s+', ' ', brand)
    title = re.sub(r'^[a-zA-Z]\s+', ' ', title)
    brand = re.sub(r'\s+[a-zA-Z]$', ' ', brand)
    title = re.sub(r'\s+[a-zA-Z]$', ' ', title)

    # stopwords
    brand = ' '.join([i.strip() for i in brand.split() if i not in
                      stop_words and i not in exclude])

    # add titles together
    if brand in title and len(brand) > 1:
        name = title
    elif len(brand.split()) > 1:
        q = [i for i in brand.split() if len(i) > 1]
        qq = [i for i in q if i in title]
        if len(q) > 0 and len(qq)/len(q) >= 0.5:
            name = title
        else:
            name = (brand + ' ' + title).strip()
    else:
        name = (brand + ' ' + title).strip()

    # remove double spaces
    name = re.sub(r'\s+', ' ', name, flags=re.I)

    # lemmatization
    sen = spacy_nlp(name)
    lem = ' '.join([token.lemma_ for token in sen])

    # stopwords
    lem_test = ' '.join([i.strip() for i in lem.split() if i not in
                         stop_words and i not in exclude])
    if len(lem) > 0 and len(lem_test) == 0:
        print('Name error: ' + lem_test)
        lem = ' '.join([i.strip() for i in lem.split() if i not in exclude])
    else:
        lem = lem_test

    # clean again
    lem = re.sub(r'(?:-PRON-)', '', lem)
    lem = re.sub(r'[\W_]', ' ', lem)
    lem = re.sub(r'\s+', ' ', lem, flags=re.I)
    lem = re.sub(r'\s+[a-zA-Z]\s+', ' ', lem)
    lem = re.sub(r'^[a-zA-Z]\s+', ' ', lem)
    lem = re.sub(r'\s+[a-zA-Z]{1,2}$', ' ', lem)

    return lem


if __name__ == '__main__':
    df = read_df()
    df = df.fillna('').apply(lambda x: x.str.strip().str.lower()
                             if x.dtype == object else x)
    df['brand_name'] = df['brand_name'].apply(lambda x: '' if x in
                                              ['generic', 'unknown'] else x)

    name = df[['brand_name', 'title']].apply(lambda x: clean(x['brand_name'],
                                                             x['title']),
                                             axis=1)
    name.name = 'name'
    cat = df['gen_cat']  # .apply(lambda x: clean('', x))
    fam = df['prod_fam']  # .apply(lambda x: clean('', x))
    typ = df['prod_type']  # .apply(lambda x: clean('', x))

    comb = pd.concat([name, cat, fam, typ], axis=1)

    df.to_csv('database.csv', index_label='key')
    comb.to_csv('clean.csv', index_label='key')
