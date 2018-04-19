
# import re
import datefinder

# string_with_dates = '''
# MSDS #: RQ1007792                                                                                             Issue Date:  09/2010 Supersedes: RQ0900706                                                                                          Issue Date:  01/2009

# '''


text_file = open("D:/Dropbox/_ICF_project/WA 2-75/HD/Delivery/Extract_summary/date_raw.txt", "r")
lines = text_file.readlines()

lines_post = []
for k in lines:
	# print "k===", k
	try:
		matches = datefinder.find_dates(k)
		# for match in matches:
		# 	print match
		matches_str = " || ".join([str(z).replace('\n', "") for z in matches])
		# print matches_str
		lines_post.append(matches_str)
	except:
		lines_post.append("N/A")

# print len(lines_post)
# print lines_post

with open("D:/Dropbox/_ICF_project/WA 2-75/HD/Delivery/Extract_summary/date_raw2.txt", 'w') as f:
    for s in lines_post:
        f.write(s + '\n')

# for match in matches:
# 	print match