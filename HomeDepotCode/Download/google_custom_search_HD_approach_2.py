# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import urllib
from collections import OrderedDict
# from xlsxwriter.workbook import Workbook


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


key_list = ['''MSDS site:http://www.homedepot.com/catalog/pdfImages''']

# Duplicate content filter. If multiple documents contain identical titles as well as 
# the same information in their snippets in response to a query, only the most relevant 
# document of that set is displayed in the results. 1-filter on; 0-filter off
filter_control=['0', '1'] 


# max returned searching results
max_results=600


csv_result_path = "D:/Dropbox/_ICF_project/WA 2-75/HD/"

for j in range(len(key_list)):

	for k in range(1):
		result_all = []
		kk = 1

		for start_index in range(0, max_results, 10):
			csv_name=csv_result_path+"Homedepot_part_"+str(kk)+'.csv'
			print csv_name

			params = OrderedDict([
			    ('q', key_list[j]),
			    ('filter', filter_control[k]),  
			    ('start', start_index),
			    ])
	
			# https://www.google.com/search?{} https://www.google.com/?gws_rd=ssl#{}
			url_1a_raw='https://www.google.com/search?{}'.format(urllib.urlencode(params))
			rep_str = {"%28": "(", "%29": ")", "%3A": ":"} # define desired replacements here
			# use these three lines to do the replacement
			rep_str = dict((re.escape(k), v) for k, v in rep_str.iteritems())
			pattern = re.compile("|".join(rep_str.keys()))
			url_1a = pattern.sub(lambda m: rep_str[re.escape(m.group(0))], url_1a_raw)
			print "url_1a", url_1a

			time.sleep(60)
			page = requests.get(url_1a)
			soup = BeautifulSoup(page.content, "lxml")
			# print soup
			all_results = soup.find_all("div", attrs={'class': "g"})

			for result in all_results:
				all_results_part1 = result.find_all("h3", class_="r")[0] #description
				all_results_part2 = result.find_all("span", class_="st")[0] #description

				# print all_results_part1
				try:
					text_temp = all_results_part1.find_all('a')[0].text.encode('ascii','ignore')
				except:
					text_temp = "N/A"
				print "text_temp====", text_temp

				try:
					pdf_raw_raw = all_results_part1.find_all('a', href=True)[0]
					pdf_url_temp = pdf_raw_raw['href'].replace("/url?q=", "").split("&sa", 1)[0]
				except:
					pdf_url_temp = "N/A"

				try:
					desc_temp = all_results_part2.text.encode('ascii','ignore')
				except:
					desc_temp = "N/A"

				result_all.append([text_temp, pdf_url_temp, desc_temp])
			# print len(result_all)

			#####write results to a CSV########
			# if start_index % 100 == 0:
			with open(csv_name, 'wb') as csvfile:
			    writer = csv.writer(csvfile)
			    writer.writerows(result_all)
			kk=kk+1
			result_all = []

