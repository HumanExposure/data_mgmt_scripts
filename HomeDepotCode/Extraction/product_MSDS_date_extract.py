# -*- coding: utf-8 -*-
import sys
import re
import os 
import xlrd
import collections

reload(sys)
sys.setdefaultencoding('utf-8')


pth = 'D:/Dropbox/_ICF_project/WA 2-75/HD/Delivery/PDF2EXCEL'
os.chdir(pth)

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

all_files = [f for f in os.listdir('.') if os.path.isfile(f)] #os.listdir(pth)
all_files = natural_sort(all_files)


# Product MSDS Data
pattern=re.compile("Date:|"\
                   "Date of issue|"\
                   "WAS PREPARED|"\
                   "Revision Date[:]*|"\
                   "Revision[:]*|"\
                   "Date Issued[:]*|"\
                   "ISSUE DATE[:]*|"\
                   "Issuing Date|"\
                   "DATE OF PREPARATION|"\
                   "DATE OF REVISION|"\
                   "Version Date|"\
                   "Date Prepared:|"\
                   "Last Updated:|"\
                   "DATE REVISED:|"\
                   "DATE PRINTED|"\
                   "DATEPREPARED|"\
                   "Date MSDS Prepared|"\
                   "DATE PREPARED|"\
                   "Revision Dale:|"\
                   "Edited on:|"\
                   "Revised on|"\
                   "Revised:|"\
                   "MSDS DATE:|"\
                   "Effective date"
                   ,re.IGNORECASE)


catch=[]
failed_name = []

# all_files=['92.xlsx']

# begin to loop through each spreadsheet by row by column
for file_ind in all_files:
    print "file===", file_ind
    catch_temp=collections.OrderedDict()
    catch_temp["file"] = file_ind
    temp_text_pool = []
    temp_text_raw = ""

    book = xlrd.open_workbook(pth+'/'+file_ind)
    for sheet in book.sheets():
        for rowidx in range(sheet.nrows):
            if rowidx <=999:
                row = sheet.row(rowidx)
                for colidx, cell in enumerate(row):
                    try:
                        if pattern.search(cell.value):
                            # catch_temp["colidx"] = colidx+1
                            # catch_temp["rowidx"] = rowidx+1
                            temp_text_raw = cell.value

                            # if catched string is very long, try to split it
                            if len(temp_text_raw) > 50:
                                split_pool = temp_text_raw.split("\n")
                                if split_pool:
                                    split_pool_2 = [k for k in split_pool if pattern.search(k)]
                                    temp_text = " || ".join(split_pool_2)
                            else:
                                temp_text = temp_text_raw

                            # if this row only contains key words (such like "product name"), get the row below also
                            if len(temp_text.split()) >= 3:
                                temp_text_out = re.sub(r'[^\x00-\x7F]+',' ', temp_text)
                            else:
                                temp_text = cell.value + " " + " ".join([k.value for k in sheet.row(rowidx+1) if len(k.value)>0])
                                temp_text_out = re.sub(r'[^\x00-\x7F]+',' ', temp_text)
                            temp_text_pool.append(temp_text_out)

                            # print "cell.value=", len(cell.value.encode('ascii','ignore').split())
                            # print "cell.value=", [k.value for k in sheet.row(rowidx+1) if len(k.value)>0]
                    except:
                        pass

    if len(temp_text_pool) >0:
        catch_temp["text"] = " ".join(temp_text_pool)
        catch_temp["auto"] = "Yes"
        catch.append(catch_temp)
        print catch_temp


    # catch empty rows
    if not any(k['file'] == file_ind for k in catch):
        failed_name.append(file_ind)
        catch.append({"file": file_ind, "text": "N/A", "auto": "No"})

# for k in catch:
#     print k

print len(failed_name), failed_name

# import unicodecsv as csv
# keys = catch[0].keys()
# with open('../Extract_summary/Product_MSDS_Date.csv', 'wb') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(catch)