ifile = open("SeventhGenerationProducts.txt",'r')
ofile = open("SeventhGenerationProducts.csv",'w')
iline = 0
for line in ifile:
    t = line.split("  ")
    t = [x for x in t if x != ""]
    t = [x.strip() for x in t]
    if len(t) == 6:
       iline += 1
       ofile.write(",".join(t)+"\n")
       print ",".join(t)
ifile.close()
ofile.close()