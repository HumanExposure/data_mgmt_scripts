import os
import string
import csv
import glob
import pandas as pd

os.chdir("C:/Users/KHAROHAL/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/WebScrapingPractice/Dormakaba Extraction/text files")

filelist = glob.glob("*.txt")

id_list = []
file_list = []
prod_names = []
doc_dates = []
rev_nums = []
raw_cats = []
raw_cas_list = []
raw_chem_names = []
funcuses = []
raw_min_comp_list = []
raw_max_comp_list = []
raw_central_comp_list = []
unit_types = []

# Functions to flatten lists of lists and format file lines neatly
def flatten_list(input_list):
    out = []
    for item in input_list:
        if isinstance(item, (list, tuple)):
            out.extend(flatten_list(item))
        else:
            out.append(item)
    return out

def cleanLine(line):
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = cline.strip('\n-')
    cline = cline.split('  ')
    cline = [cline[0]] + [p.strip() for p in cline[1:] if (
                p != "")]
    return (cline)

for file in filelist:
    #print(file)
    ID = ''
    prod_name = ''
    doc_date = ''
    rev_num = ''
    raw_cat = ''
    raw_cas = []
    raw_chem_name = []
    reported_funcuse = []
    min_comp = []
    max_comp = []
    central_comp = []
    unit = ''
    rank = ''

    # open and read factotum csv to get id numbers
    template = csv.reader(open(
        'C:/Users/KHAROHAL/OneDrive - Environmental Protection Agency (EPA)/Profile/Downloads/unextractedIDs.csv'))
    for row in template:
        if row[1] == file.replace('txt','pdf'):
            ID = row[0]
            break
        if ID == '':
            continue

    ifile = open(file, encoding='utf8')
    for line in ifile:
        cline = cleanLine(line)
        if cline == [] or cline == '':
            continue

        # product name
        if len(cline) > 1 and prod_name == '':
            prod_name = ''.join(cline[0])

        # document date
        for date in cline:
            if "published " in date and doc_date == '':
                doc_date = ''.join(date[date.index("published ")+16:])

        # version numbers
        if len(cline) > 1:
            for vers in cline:
                if "declaration" in vers and rev_num == '':
                    rev_num = ''.join(vers[vers.index("declaration ") + 12:])

        # raw categories, can update by removing numbers
        for category in cline:
            if 'classification: ' in category and raw_cat == '':
                raw_cat = ''.join(category[category.index(': ') + 2:])
                #split_cat = raw_cat.split()
                #for char in split_cat:
                    #if char.isnumeric() == True:
                        #split_cat.remove(char)

        # chem names, still need to fix multiline names
        if any('id:' in cas for cas in cline) or any('%:' in per for per in cline):
            if cline[0] == '' and '%: ' not in cline[1]:
                raw_chem_name.append(''.join(cline[1:-1]))
            elif '%: ' in cline[1] and cline[0] != '':
                raw_chem_name.append(''.join(cline[0:-1]))
                raw_cas.append('')
            elif '%: ' in cline[1] and cline[0] == '' or '%: ' in cline[0]:
                pass
            else:
                raw_chem_name.append(''.join(cline[0:-1]))
        # 632 total chemicals, including without CAS

        # cas numbers
        if any('id:' in cas for cas in cline):
            raw_cas.append(cline[-1].replace('id: ', ''))
            # 621 chemicals with CAS numbers

        # reported functional use
        if any('residuals and impurities' in c for c in cline):
            mat_type_flag = True
        if 'ppm' in cline:
            mat_type_flag = False
        if (any('substance' in func for func in cline) and any('role:' in func for func in cline) or
                any('material' in f for f in cline) and any('role:' in f for f in cline) or
                any('material' in m for m in cline) and any('type:' in t for t in cline)):
            if 'substance role: ' in cline[-1]:
                reported_funcuse.append(cline[-1].replace('substance role: ', ''))
            elif 'substance role:' in cline[-2]:
                reported_funcuse.append(' '.join(cline[-2:]).replace('substance role: ', ''))
            elif 'substance role:' in cline[-3]:
                reported_funcuse.append(' '.join(cline[-2:]))
            elif 'role:' in cline[-3]:
                reported_funcuse.append(' '.join(cline[-2:]))
            elif 'role:' in cline[-2]:
                reported_funcuse.append(cline[-1])
            elif 'role:' in cline[-1]:
                reported_funcuse.append(cline[-1].replace('role: ', '').replace('material ', ''))
            elif 'material role:' in cline[-1]:
                reported_funcuse.append(cline[-1].replace('material role: ', ''))
            elif 'material role:' in cline[-2]:
                reported_funcuse.append(' '.join(cline[-2]).replace('material role: ', ''))
            elif 'material role:' in cline[-3]:
                reported_funcuse.append(' '.join(cline[-2:]))
            else:
                reported_funcuse.append(''.join(cline[-1]).replace('material type: ', ''))

        # raw min and max composition
        if any('%:' in p for p in cline):
            # for min and max comps
            if '%: ' in cline[0] and '-' in cline[0]:
                split_cline = cline[0].split()
                min_comp.append(split_cline[1])
                max_comp.append(split_cline[3])
                central_comp.append('')
            elif '%: ' in cline[1] and '-' in cline[1]:
                sec_split_cline = cline[1].split()
                min_comp.append(sec_split_cline[1])
                max_comp.append(sec_split_cline[3])
                central_comp.append('')
            # for central comps
            elif '%: ' in cline[0] and '-' not in cline:
                central_split_zero = cline[0].split()
                central_comp.append(central_split_zero[1])
                min_comp.append('')
                max_comp.append('')
            elif '%: ' in cline[1] and '-' not in cline:
                central_split_one = cline[1].split()
                central_comp.append(central_split_one[1])
                min_comp.append('')
                max_comp.append('')
        # unit type
        if any('%:' in percent for percent in cline):
            unit_types.append('3')

    # keep these at the end, inside only 1st for loop
    funcuses.append(reported_funcuse)
    raw_chem_names.append(raw_chem_name)
    raw_cas_list.append(raw_cas)
    raw_min_comp_list.append(min_comp)
    raw_max_comp_list.append(max_comp)
    raw_central_comp_list.append(central_comp)
    n = len(raw_chem_name)
    prod_names.append([prod_name]*n)
    doc_dates.append([doc_date]*n)
    rev_nums.append([rev_num]*n)
    raw_cats.append([raw_cat]*n)
    file_list.append([file]*n)
    id_list.extend([ID]*n)

# ingredient rank
ingredients_rank = [[index+1 for index, k in enumerate(sublist)] for sublist in raw_chem_names]

flat_file_list = flatten_list(file_list)
flat_id_list = flatten_list(id_list)
flat_prod = flatten_list(prod_names)
flat_dates = flatten_list(doc_dates)
flat_revs = flatten_list(rev_nums)
flat_cats = flatten_list(raw_cats)
flat_cas = flatten_list(raw_cas_list)
flat_chem_names = flatten_list(raw_chem_names)
flat_funcuses = flatten_list(funcuses)
flat_min_comp = flatten_list(raw_min_comp_list)
flat_max_comp = flatten_list(raw_max_comp_list)
flat_units = flatten_list(unit_types)
flat_ingredients = flatten_list(ingredients_rank)
flat_central_comp = flatten_list(raw_central_comp_list)

factotum_df = pd.DataFrame({
    'data_document_id': flat_id_list,
    'data_document_filename': flat_file_list,
    'prod_name': flat_prod,
    'doc_date': flat_dates,
    'rev_num': flat_revs,
    'raw_category': flat_cats,
    'raw_cas': flat_cas,
    'raw_chem_name': flat_chem_names,
    'report_funcuse': flat_funcuses,
    'raw_min_comp': flat_min_comp,
    'raw_max_comp': flat_max_comp,
    'unit_type': flat_units,
    'ingredient_rank': flat_ingredients,
    'raw_central_comp': flat_central_comp
})

print(factotum_df)
factotum_df.to_csv("C:/Users/KHAROHAL/OneDrive - Environmental Protection Agency (EPA)/Profile/Downloads/Factotum_Dormakaba_HPD_extracted_documents.csv",
                   index=False, encoding='utf-8-sig')
