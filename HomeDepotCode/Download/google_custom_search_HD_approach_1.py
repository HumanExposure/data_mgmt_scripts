# -*- coding: utf-8 -*-
import pprint
import csv
from googleapiclient.discovery import build
import time



# Build a service object for interacting with the API. Visit
# the Google APIs Console <http://code.google.com/apis/console>
# to get an API key for your own application.
# https://developers.google.com/custom-search/json-api/v1/reference/cse/list#parameters

service = build("customsearch", "v1",
          developerKey="")

csv_result_path = "D:/Dropbox/_ICF_project/WA 2-75/HD/"

result_all = []


for kk in range(0, 100):
    print "kk=====", kk
    result_all = []
    for page_index in range(1,11):
        print "page_index=======", page_index
        csv_name=csv_result_path+"Homedepot_term1_filter_on_part_"+str(kk)+'.csv'

        res = service.cse().list(
            q = '''MSDS site:http://www.homedepot.com/catalog/pdfImages''',
            cx = '',
            filter = '1',
            safe = 'off',
            fileType = "pdf",
            num = 10,
            start = (page_index-1)*10+1,
            lowRange = kk*100,
            highRange = (kk+1)*100
          ).execute()
        # response = res.execute()
        # print res.to_json()
        # pprint.pprint(res)

        results_all_raw = res['items']
        for results_ele_raw in results_all_raw:
            try:
                text_temp = results_ele_raw['title'].encode('ascii','ignore')
            except:
                text_temp = "N/A"

            try:
                pdf_url_temp = results_ele_raw['link']
            except:
                pdf_url_temp = "N/A"

            try:
                desc_temp = results_ele_raw['snippet'].encode('ascii','ignore')
            except:
                desc_temp = "N/A"
            result_all.append([text_temp, pdf_url_temp, desc_temp])
        # time.sleep(3)
    with open(csv_name, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result_all)
