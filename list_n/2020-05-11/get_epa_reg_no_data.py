# -*- coding: utf-8 -*-
"""Do things.

Created on Wed Apr  1 11:57:12 2020

@author: SBURNS
"""


import requests
from bs4 import BeautifulSoup
import unicodedata
import time
import random

import pandas as pd
import os


def get_url(x):
    """Get url of fancy EPA number."""
    time.sleep(random.random()+1)
    r = requests.get('https://iaspub.epa.gov/apex/pesticides/' +
                     'f?p=PPLS:102:::NO::P102_REG_NUM:' + x)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
    else:
        print('Fail: ' + x)
        return None

    try:
        top_row = soup.find(id='tab-1') \
            .find(class_='uReport uReportStandard').tbody.tr.find_all('td')

        reg_no = top_row[0].get_text().strip()
        if reg_no != x.strip():
            print('Reg no does not match: ' + x)
            return None
        prod_name = top_row[1].get_text().strip()
        date = top_row[2].get_text().replace('(PDF)', '').strip()
        url = unicodedata.normalize('NFKD', top_row[2].a['href']).strip()
    except (AttributeError, TypeError):
        print('Fail: ' + x)
        return None

    # get chemical data
    try:
        table = soup.find(id='tab-2').find('table',
                                           class_='uReport uReportStandard')
        chem_table = unicodedata.normalize('NFKD', str(table))
        df = pd.read_html(chem_table)[0]
    except (TypeError):
        print('Failed Table Extraction: ' + x)
        df = None
    return [reg_no, prod_name, date, url, df]


def write_pdf(url, label):
    """Write PDF file."""
    # if url is None:
    #     return None

    # filename = url.split('/')[-1]
    filename = os.path.basename(url)
    fpath = os.path.join('pdfs_' + label, filename)
    if os.path.exists(filename):
        return filename, True

    r = requests.get(url)
    with open(fpath, 'wb') as f:
        f.write(r.content)

    return filename, False


def write_data(row, col, label, reset):
    """Write data for document."""
    x = row[col]
    data = get_url(x)
    if data is None:
        return [x, '', '', '', '', '']
    filename, exists = write_pdf(data[3], label)
    if exists and not reset:
        print('Already exists: ' + x)
        return [x, 'ALREADY EXISTS', '', '', '', '']
    if data[4] is None:
        return [x, data[1], data[2], '', filename, data[3]]
    fname = os.path.splitext(filename)[0] + '.csv'
    data[4].to_csv(os.path.join('chems_' + label, fname), index=False)
    print('Success: ' + x)
    return [x, data[1], data[2], fname, filename, data[3]]


def read_files(input_file, old_list, date, old_date, reg_no_col, date_col):
    """Get the list of files that need to be read."""
    df = pd.read_csv(input_file)  # input_file
    if old_list is None:
        return df
    df_old = pd.read_csv(old_list)  # old input file

    # reg nos that aren't in the old list. probably don't need this
    df_new = df.loc[~df[reg_no_col].isin(df_old[reg_no_col])]

    # entries that are newer than the old list
    dcol = pd.to_datetime(df[date_col])
    df_updated = df.loc[dcol >= pd.to_datetime(old_date)]

    df_comb = pd.concat([df_new, df_updated]).drop_duplicates()
    return df_comb


def run_functions(input_file, old_list, date, old_date, label,
                  reg_no_col, date_col, reset):
    """Run everything."""
    if not os.path.isdir('pdfs_' + label):
        os.mkdir('pdfs_' + label)
    if not os.path.isdir('chems_' + label):
        os.mkdir('chems_' + label)

    df = read_files(input_file, old_list, date, old_date, reg_no_col, date_col)

    df_info = df.apply(write_data, axis=1, result_type='expand',
                       args=(reg_no_col, label, reset,))
    df_info.rename(columns={0: 'reg_no', 1: 'product_name', 2: 'date',
                            3: 'chem_filename', 4: 'pdf_filename',
                            5: 'pdf_url', }, inplace=True)
    df_info.to_csv(label + '_extracted_info_' + date + '.csv', index=False)


if __name__ == '__main__':
    # change these values
    label = 'list_n'  # e.g. list_n
    old_date = '2020-05-01'
    date = '2020-05-11'

    # input_file = 'list_n.csv'  # file with epa reg nos
    # set old_list to none if you want to read all of them
    input_file = os.path.join(
        'documents', date, 'List N Disinfectants for Use Against ' +
        'SARS-CoV-2  Pesticide Registration  US EPA.csv')
    old_list = os.path.join(
        'documents', old_date, 'List N Disinfectants for Use Against ' +
        'SARS-CoV-2  Pesticide Registration  US EPA.csv')
    reg_no_col = 'EPA Registration Number'  # column with reg nos
    date_col = 'Date Added to List N'
    reset = True

    run_functions(input_file, old_list, date, old_date, label,
                  reg_no_col, date_col, reset)
