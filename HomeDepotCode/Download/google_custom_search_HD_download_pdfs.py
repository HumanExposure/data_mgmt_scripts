#!/usr/bin/python
# download product PDFs
############################################
import re
import csv
import time
import urllib

all_title = []
all_url = []
all_desc = []
all_pdf = []
all_failed = []

with open("D:/Dropbox/_ICF_project/WA 2-75/HD/all_final.csv", 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        all_title.append(row[0])
        all_url.append(row[1])
        all_desc.append(row[2])
# 

for k in range(len(all_title)):
    time.sleep(3)
    print k
    pdf_url = all_url[k]
    print pdf_url
    if pdf_url == "N/A":
        all_pdf.append("N/A")
    else:
        pdf_name_temp = k+1
        all_pdf.append(str(pdf_name_temp)+".pdf")
        try:
            testfile = urllib.URLopener()
            testfile.retrieve(pdf_url, "D:/Dropbox/_ICF_project/WA 2-75/HD/MSDS_pdfs/"+str(pdf_name_temp)+".pdf")
        except:
            print "failed", pdf_url
            all_failed.append(pdf_url)

output_context = zip(*[all_title, all_url, all_desc, all_pdf])

with open("D:/Dropbox/_ICF_project/WA 2-75/HD/all_final_1.csv",'wb') as outF:
    writer = csv.writer(outF)
    writer.writerows(output_context)

print "all_failed====", all_failed