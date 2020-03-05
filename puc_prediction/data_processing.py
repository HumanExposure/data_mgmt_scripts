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
from pymysql import escape_string

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
    """
    The reason this statement looks so ugly it because it deals with
    products that have more than 1 puc. It will only include products that
    have a classification method of 'MA' or 'MB' and will prioritize 'MA'.
    """
    sqq = 'SELECT puc_id, product_id, brand_name, title, gen_cat, ' + \
          'prod_fam, prod_type, description ' + \
          'FROM ( SELECT brand_name, title, puc_id, product_id ' + \
          'FROM (select id, brand_name, ' + \
          'title from dashboard_product) as product ' + \
          'INNER JOIN (' + \
          'select product_id, puc_id from (' + \
          '(select x1.product_id, puc_id, classification_method, ' + \
          'classification_confidence as done from (select product_id, ' + \
          'count(puc_id) from dashboard_producttopuc group by product_id ' + \
          'having count(puc_id) > 1) as x1 INNER JOIN (select * from ' + \
          'dashboard_producttopuc where classification_method = "MA") as ' + \
          'x2 on x1.product_id = x2.product_id) UNION (select ' + \
          'q3.product_id, puc_id, classification_method, ' + \
          'classification_confidence as done from (select q6.product_id ' + \
          'from (select q1.product_id, classification_confidence as done ' + \
          'from (select product_id from dashboard_producttopuc group by ' + \
          'product_id having count(puc_id) > 1) as q1 INNER JOIN (select ' + \
          '* from dashboard_producttopuc where classification_method = ' + \
          '"MA") as q2 on q1.product_id = q2.product_id) as q5 RIGHT JOIN ' + \
          '(select product_id from dashboard_producttopuc group by ' + \
          'product_id having count(puc_id) > 1) as q6 on q5.product_id = ' + \
          'q6.product_id where done is null) as q3 INNER JOIN (select * ' + \
          'from dashboard_producttopuc where classification_method = "MB")' + \
          ' as q4 on q3.product_id = q4.product_id) UNION (select ' + \
          'r1.product_id, puc_id, classification_method, ' + \
          'classification_confidence as done from ((select product_id ' + \
          'from dashboard_producttopuc group by product_id having ' + \
          'count(puc_id) = 1) as r1 INNER JOIN (select * from ' + \
          'dashboard_producttopuc where classification_method = "MB" or ' + \
          'classification_method = "MA") as r2 on r1.product_id = ' + \
          'r2.product_id))) as prod_to_puc_temp) as prod_to_puc ' + \
          'ON product.id = prod_to_puc.product_id ) as product_match ' + \
          'INNER JOIN (select * from dashboard_puc) as puc ' + \
          'ON product_match.puc_id = puc.id;'
    df = pd.read_sql(sqq, engine)
    engine.dispose()
    return df.fillna('')


def read_group(group):
    """Read df of brand name and puc from factotum."""
    with open('mysql.json', 'r') as f:
        cfg = json.load(f)['mysql']
    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           convert_unicode=True, echo=False)
    sqq = 'select product_id as id, brand_name, title, data_group_id from ' + \
          '(select DISTINCT product_id as p2 from dashboard_producttopuc) ' + \
          'as q1 RIGHT JOIN (SELECT DISTINCT product_id, brand_name, ' + \
          'title, data_group_id FROM (SELECT product_id, brand_name, ' + \
          'title, document_id FROM (SELECT id, brand_name, title FROM ' + \
          'dashboard_product) AS p1 INNER JOIN (SELECT document_id, ' + \
          'product_id FROM dashboard_productdocument) AS p2 ON p1.id = ' + \
          'p2.product_id) AS p3 INNER JOIN (SELECT id as d_id, ' + \
          'data_group_id FROM dashboard_datadocument ' + \
          f'WHERE data_group_id = {group}) ' + \
          'AS p4 ON p3.document_id = p4.d_id) as q2 on q1.p2 = ' + \
          'q2.product_id where p2 is null;'
    df = pd.read_sql(escape_string(sqq), engine)
    engine.dispose()
    return df.fillna('')


def read_extracted(group):
    """Read extracted text from a group (for group with no products).

    This is a temporary function and should only be used for testing.
    """
    with open('mysql.json', 'r') as f:
        cfg = json.load(f)['mysql']
    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           convert_unicode=True, echo=False)
    sql = 'SELECT d_id, prod_name, data_group_id FROM (SELECT ' + \
          'data_document_id, prod_name FROM dashboard_extractedtext) ' + \
          'AS p1 INNER JOIN (SELECT id AS d_id, data_group_id FROM ' + \
          f'dashboard_datadocument WHERE data_group_id = {group}) ' + \
          'AS p2 ON p1.data_document_id = p2.d_id;'
    df = pd.read_sql(escape_string(sql), engine)
    engine.dispose()
    df = df.rename(columns={'d_id': 'id', 'prod_name': 'title'})
    df['brand_name'] = ''
    df = df[['id', 'brand_name', 'title', 'data_group_id']]
    return df.fillna('')


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
        print('Name error: ' + lem + ' - ' + lem_test)
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

    return lem.strip()
