# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 11:40:36 2022

@author: ALarger
"""

import csv, os


lines = list()
rownumbers_to_remove= [461, 463, 466, 581, 622, 954, 1011, 1012, 1013, 1014, 1062, 1063, 1064, 1212, 1213, 1214, 1477, 1568, 2725, 2726, 2727, 2728, 2730, 2731, 2734, 2735, 2736, 2738, 2739, 2740, 2741, 2742, 2753, 2754, 2755, 2756, 2757, 2758, 2759, 2760, 2761, 2762, 2763, 2764, 2765, 2766, 2767, 2768, 2769, 2771, 2772, 2773, 2774, 2775, 2777, 2778, 2779, 2780, 2781, 2782, 2783, 2784] #rows as printed in factotum error message
rownumbers_to_remove = [x + 1 for x in rownumbers_to_remove]

path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chemical curation upload\2024-05-29\uploads'
filename = 'DSSTox_Factotum_uncurated_chemicals_37-04302024xlsx_formatted_3.csv'

os.chdir(path)

with open(filename, 'r') as read_file:
    reader = csv.reader(read_file)
    for row_number, row in enumerate(reader, start=1):
        if(row_number not in rownumbers_to_remove) and (all(x in '1234567890 ' for x in str(row[0])) or row[0] == 'external_id'):
            lines.append(row)

with open(filename.split('.csv')[0]+'_removed.csv', 'w', newline='') as write_file:
    writer = csv.writer(write_file)
    writer.writerows(lines)
