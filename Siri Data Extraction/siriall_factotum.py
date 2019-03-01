# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 08:43:11 2019

@author: ALarger
"""

import csv
import pandas as pd

with open(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\siriall copy.csv','r') as siriall:
    reader = csv.reader(siriall)
    names = []
    filenames = []
    titles = []
    doctypes = []
    urls = []
    organizations = []
    i = 0
    for row in reader:
        name = row[21]
        if '.html' in name:
            if name in names:
                continue
            else:
                names.append(name)
        else:
            continue
        filenames.append(name.replace('.html','.pdf'))
        titles.append(row[2])
        doctypes.append('2')
        urls.append(row[5])
        organizations.append(row[3])
        i = i + 1
        print(i/252753*100,'%')
#        if i > 10:
#            break
df = pd.DataFrame({'filename': filenames, 'title': titles, 'document_type': doctypes, 'url': urls, 'organization': organizations})
df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\siriall_template.csv', index=False)