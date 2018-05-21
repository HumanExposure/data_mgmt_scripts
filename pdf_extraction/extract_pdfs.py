import pymysql
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import yaml

# This script should be run from within a directory full of PDFs that you want to extract text from and load
# into mysql db

# grab config settings from config.yml. This file should be in the same dir where the this script is run from. See
# README.md for details in making config.yml
with open("config.yml", 'r') as ymlfile:
	cfg = yaml.load(ymlfile)

# The datagroup id for the directory of pdfs you are looking at and the path to that directory go in these variables
DATAGROUP_ID = '19'
DIRECTORY = "/data/code/factotum/media/Walmart_MSDS_3/pdf"

# Setup database connection
connection_r = pymysql.connect(host=cfg['mysql']['host'],
							   port=3306,
							   user=cfg['mysql']['user'],
							   db='prod_factotum',
							   password=cfg['mysql']['password'],
							   use_unicode=True,
							   charset='utf8')

# set up cursor
connection_w = pymysql.connect(host=cfg['mysql']['host'],
							   port=3306,
							   user=cfg['mysql']['user'],
							   db='prod_pdf_txt',
							   password=cfg['mysql']['password'],
							   use_unicode=True,
							   charset='utf8')

cursor_r = connection_r.cursor()
cursor_w = connection_w.cursor()

# This function takes in the full path to a file (pdf) and returns the text found in the pdf
def convert_pdf_to_txt(path):
	rsrcmgr = PDFResourceManager()
	retstr = StringIO()
	codec = 'utf-8'
	laparams = LAParams()
	device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
	fp = file(path, 'rb')
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	password = ""
	maxpages = 0
	caching = True
	pagenos = set()

	for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
								  check_extractable=True):
		interpreter.process_page(page)

	text = retstr.getvalue()

	fp.close()
	device.close()
	retstr.close()
	return text


#####  This is where everything starts

# create an array of all pdfs from DIRECTORYil
all_files = []
for dirpath, dirnames, filenames in os.walk(DIRECTORY):
	for filename in [f for f in filenames if f.endswith(".pdf")]:
		f = filename
		p = os.path.join(dirpath, filename)
		all_files.append({'filename': f, 'path': p})

good_pdf_count = 0
bad_pdf_count = 0

for pdf in all_files:
	print(pdf['path'])
	print("Current pdf count is " + str(good_pdf_count + bad_pdf_count))
	print(str(bad_pdf_count) + " pdfs are not processable")
	try:
		pdf_contents = convert_pdf_to_txt(pdf['path'])
		# pdf_contents = "test"
		pdf_contents = pdf_contents.replace('"', '')
		pdf_contents = pdf_contents.replace("'", "")
		sql_r = "SELECT * FROM dashboard_datadocument WHERE filename = '" + pdf['filename'] + \
				"' AND data_group_id = " + DATAGROUP_ID
		cursor_r.execute(sql_r)
		result = cursor_r.fetchone()
		if result:
			print(result[0])
			sql_w = "INSERT INTO pdfs (factotum_datadocument_id, factotum_datagroup_id, filename, " \
					"pdf_contents) VALUES (" + str(result[0]) + ", DATAGROUP_ID, '" + pdf['filename'] + "', '" + \
					pdf_contents + "')"
			# print(sql_w)
			cursor_w.execute(sql_w)
			connection_w.commit()
		else:
			print('File not found in factotum.')
		good_pdf_count += 1
	except:
		# print("Unable to convert the pdf.")
		bad_pdf_count += 1

print(len(all_files))
print("Good pdfs: " + str(good_pdf_count))
print("Bad pdfs: " + str(bad_pdf_count))

connection_w.close()
connection_r.close()
