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
    if url is None:
        return None

    # filename = url.split('/')[-1]
    filename = os.path.basename(url)
    r = requests.get(url)

    with open(os.path.join('pdfs_' + label, filename), 'wb') as f:
        f.write(r.content)

    return filename


def write_data(row, col, label):
    """Write data for document."""
    x = row[col]
    data = get_url(x)
    if data is None:
        return [x, '', '', '', '', '']
    filename = write_pdf(data[3], label)
    if data[4] is None:
        return [x, data[1], data[2], '', filename, data[3]]
    fname = os.path.splitext(filename)[0] + '.csv'
    data[4].to_csv(os.path.join('chems_' + label, fname), index=False)
    print('Success: ' + x)
    return [x, data[1], data[2], fname, filename, data[3]]


def run_functions(input_file, label, reg_no_col):
    """Run everything."""
    if not os.path.isdir('pdfs_' + label):
        os.mkdir('pdfs_' + label)
    if not os.path.isdir('chems_' + label):
        os.mkdir('chems_' + label)

    df = pd.read_csv(input_file)  # input_file
    df_info = df.apply(write_data, axis=1, result_type='expand',
                       args=(reg_no_col, label,))
    df_info.rename(columns={0: 'reg_no', 1: 'product_name', 2: 'date',
                            3: 'chem_filename', 4: 'pdf_filename',
                            5: 'pdf_url', }, inplace=True)
    df_info.to_csv(label + '_extracted_info.csv', index=False)


if __name__ == '__main__':
    # change these values
    label = 'list_n'  # e.g. list_n
    input_file = 'list_n.csv'  # file with epa reg nos
    reg_no_col = 'EPA Registration Number'  # column with reg nos

    run_functions(input_file, label, reg_no_col)
