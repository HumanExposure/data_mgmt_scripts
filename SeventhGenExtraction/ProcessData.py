import os,sys,string
from glob import glob
from shutil import move, copy

    

def pdf_to_text(files):

    execfile = "pdftotext.exe"
    
    for file in files:
        pdf = '"'+file+'"'
        cmd = " ".join([execfile,"-layout","-nopgbrk",pdf])
        print cmd
        os.system(cmd)
    return
    
def text_to_csv(files):
    print "here"
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    ofile = open("SeventhGenerationProducts.txt","w")
    ofile.write("ChemicalName    CAS    FunctionalUse    Concentration    LD50\n")
    for file in files:
      # if file == files[0]:
         ifile = open(file,'r')
         record = False
         nlines = 0
         # print "\n\n\n"
         for line in ifile:
             if line == "\n": continue
             # cline = clean(line)
             cline = line.strip()
             tline = cline.lower()
             tline = tline.replace(" ","")
             if record: 
                if ("section4:" in tline):
                   record = False
                   continue
                if ("page" in tline): continue
                if ("    " in cline):
                   if (cline[0][0] == "*"):continue
                   ofile.write(cline + "    "+file[:-4]+".pdf\n")
                   print cline
                   # cline = cline.split("  ")
                   # cline = [x for x in cline if x != ""]
                   # cline = [x.strip() for x in cline]
                   # if (len(cline) != 5): print cline
                   
             if not record:
                if ("ingredientfunctioncasnumberconcentration1ld502" in tline): record = True
         ifile.close()
    ofile.close()
    return


def main():
    os.chdir("C:/Users/kphillip/Documents/SeventhGenerationSDS/")
    pwd = os.getcwd()
    
    file_list = glob("sds_*.pdf")
    n_pdfs = len(file_list)
    n_txts = len(glob("sds_*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(file_list)
    
    n_txts = len(glob("sds_*.txt"))
    if (n_txts == n_pdfs):
       file_list = glob("*.txt")
       text_to_csv(file_list)
    file_list = glob("MSDS_*.pdf")
    
    return
    
if __name__ == "__main__": main()