# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 08:28:30 2019

@author: ALarger

Checks entries in siriall.csv to see if they have corresponding html files
"""

import csv, os

with open(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\siriall copy.csv','r') as siriall:
    with open(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\siriall_new.csv', 'w') as siriall_new:
        writer = csv.writer(siriall_new, lineterminator='\n')
        reader = csv.reader(siriall)
        
        all = []
        i = 0
        
        for row in reader:
            url = row[5].split('/')
            if i == 0:
                row.append('html_file_in_folder')
                row.append('filename')
            try:
                path = 'L://Lab//NCCT_ACToR//BUILD_2019Q1//data_collection_data//siri.org//DataPrep//msds//' + url[4] + '//siri.org//msds//' + url[4] + '//' + url[5] + '//' + url[6]
                if os.path.isfile(path) == True:
                    row.append('yes')
                    row.append(url[6])
                else:
                    row.append('no')
            except IndexError:
                pass
#            if i == 10:
#                break
            print(i/799754*100, '%')
            i = i + 1
            all.append(row)
        writer.writerows(all)