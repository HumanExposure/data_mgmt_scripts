#lkoval
#5-4-2020

import pandas as pd
import os
import string
import re


os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents//FUse")

#Converts the pdf into a text file so it can be parsed
# pdf="IngredientSearch_ACI.pdf"
# execfile="pdftotext" #pdftotext application
# execpath="//home//lkoval//xpdf-tools-linux-4.01//bin64" #pdftotext application path
#
# cmd=os.path.join(execpath,execfile)
# cmd=" ".join([cmd,"-nopgbrk","-table",pdf])
# os.system(cmd) #convert pdf to txt file

text_file="IngredientSearch_ACI.txt"

ifile=open(text_file, encoding='cp1252') #some characters were not utf-8 so encoding is now Windows-1252
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #clean function to remove non-printable characters

#initialize lists to store data
raw_chem_name=[]
raw_cas=[]
reported_funcuse=[]

cas_pattern=re.compile('^\d+-{1}\d{2}-{1}\d{1}') #used to identify cas numbers in the cleaned lines

alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

letter_start=["8021-27-0","na","12239-13-3","87246-72-8","na","na","706-14-9","120-57-0","8007-70-3","8022-96-6","1332-58-7","50-21-5","12511-31-8","12225-18-2","8015-73-4",
"99-87-6","14808-60-7","84775-94-0","na","10543-57-4","57455-37-5","121-33-5","67701-05-7","11138-66-2","no-y","1318-02-1"]

letter_stop=["26658-46-8","80-54-6","8007-02-1","9014-92-0","97-53-0","110-17-8","8001-29-4","12122-17-7","9043-30-5","8000-27-9","na","223749-79-9","8007-12-3",
"9016-45-9","37251-67-5","90082-43-2","68990-67-0","8000-25-7","8002-74-2","139-89-9","68555-36-2","67701-05-7","67701-05-7","11138-66-2","no-y","supporting"]

#tuple of the letter and the cas numbers where the chemical names starting with that letter start and stop.
letter_range=tuple(zip(alphabet,letter_start,letter_stop))

#words that indicate functional use. Used to seperate chemical names and functional use information if rows were split into multiple lines.
use_keys=["agent","regulator","emulsifier,","otherwise","bleaching-","stabilizing","oxidizing","bulking", "inhibitor","listed","absorbent","antiredeposition","fragrance","solvent"]

#other observed characters that appear as the first element in a line. Only used as a check for chemicals that start with a letter and whose names are split into multiple lines
symbols=["(",")","[","]","."]

#Two observed cases where a chemical name is split onto multiple lines but the first line doesn't contian the cas used to flag the start
dif_start=["n-(4-chloro-2,5-dimethoxyphenyl)-2-[[2,5-","raphanus"]





############################ Extracts Chemicals where chemical name starts with a number  ################################
start=False
cas_flag_1=False #flag that tells if a cas number is found in the cleaned line
cas_flag_2=False # flag that tells if the line containg a cas should be the first "entry" for a chemical in the list or all the info should be added to the existing chemical entry that was split into multiple lines
cas_flag_3=False #flag that tells if a cleaned line is the first part of a chemical name but the cas is not in the line
for line in ifile:#loop through each line in file
    if line=='\n': continue
    cline=clean(line)
    cline=cline.lower()
    cline=cline.replace('.',",")
    cline=cline.replace(';',',')
    cline=cline.strip()
    cline=cline.split(" ")
    cline = [x.strip() for x in cline if x != ""]
    if ("ingredient" and "cas" and "function" in cline) and (len(cline)<10): #another line in the file contained all the words in the column headers so set the start at table, not other line
        start=True
    elif "8021-27-0" in cline: #stop looking when chemical names stop beginning with numbers
        start=False
    if start==True:#Start looking at lines in file
        if (cline[0][0] in alphabet) and (cline[0] not in use_keys):# if the first character of the line is a letter and the first word is not a functional use then this is the split chem name that needs to be added on to previous chemical name. Check for a cas number.
            cas_flag_1=False #assume no cas in line and then check
            for word in cline:
                if bool(cas_pattern.match(word)):#if a cas is in the line, get its location in the line and set cas_flag_1 to True to reflect the presence of the cas. This usually indicates that functional use is in the line too.
                    cas_index=cline.index(word)
                    cas_flag_1=True
                    break
            if cas_flag_1==True:#if a cas is in the line, then add the piece of the chemical name on the current line to the previous entry in the name list and assign the cas and func use from current line as the values for the previous entry in the cas and functional use lists.
                raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline[:cas_index])
                raw_cas[-1]=cline[cas_index]
                reported_funcuse[-1]=" ".join(cline[cas_index+1:])
            else:#if a cas is not in the line then only add the piece of the chemical name on the current line to the previous entry in the name list
                try:
                    raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline)
                    cas_flag_2=False
                except:
                    continue
        elif (cline[0][0] in alphabet) and (cline[0] in use_keys):# if the first character in the line is a letter and the first word is a functional use, edit the previous functional use
            reported_funcuse[-1]=reported_funcuse[-1]+" "+" ".join(cline)
            cas_flag_2=False
        elif cline[0][0] not in alphabet:#if the first character is non-alphabetic then it is most likely, but not always, a new chemical name.
            cas_flag_1=False #assume no cas in line
            for word in cline:
                if bool(cas_pattern.match(word)):#if a cas is in the line, get the location of the cas in the line and set cas_flag_1 to True to reflect the presence of the cas
                    cas_index=cline.index(word)
                    cas_flag_1=True
                    break
            if cas_flag_1==True and cas_flag_3==False:#if a cas is in the line and it is a new chemical name then add the chemical name, the cas, and the functional use to the appropriate list. Flip cas_flag_2 to True. In case any info is split onto the next line, this flag indicates data should be appended onto existing entries.
                raw_chem_name.append(" ".join(cline[:cas_index]))
                raw_cas.append(cline[cas_index])
                reported_funcuse.append(" ".join(cline[cas_index+1:]))
                cas_flag_2=True
            elif cas_flag_1==True and cas_flag_3==True:#if the cas is in the line and it isn't a new chemical name, append the chemical name and functional use onto the previous entry in the appropriate list and make the cas entry from the previous list the current cas. Flip cas_flag_2 to True. In case any info is split onto the next line, this flag indicates data should be appended onto existing entries. Keep cas_flag_3 at False because this isn't a new chemical name
                raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline[:cas_index])
                raw_cas[-1]=cline[cas_index]
                reported_funcuse[-1]=" ".join(cline[cas_index+1:])
                cas_flag_2=True
                cas_flag_3=False

            if (cas_flag_1==False and cas_flag_2==True) and cline[0][0]=="7":#Single special instance of a new chemical name without any other info in line. Needs to be its own new entry not appeneded on to an exiksting one. Flip cas_flag_3 to True to indicate that we are missing a cas for a new chemical entry
                raw_chem_name.append(" ".join(cline))
                raw_cas.append("")
                reported_funcuse.append("")
                cas_flag_3=True
            elif cas_flag_1==False and cas_flag_2==True:#if a cas is not in the line line and it is not a new chemical name, append the chemical name onto the previous entry in the list
                raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline)
                cas_flag_2=False
            elif cas_flag_1==False and cas_flag_2==False:#if a cas is not in the line and it is a new checmical name, add the chemical name to the name list and add empty strings to the cas and functional use lists to maintain the same length.
                raw_chem_name.append(" ".join(cline))
                raw_cas.append("")
                reported_funcuse.append("")



############################ Extracts Chemicals Where Chemical Name Starts With A Letter###################################

"""
the letter_range list containts tuples of each letter of the alphabet and the cas numbers where chemical names that start with each letter start and stop on the pdf. Since the chemicals are in alphabetical order, I tested the first letter of the line which helped me identify which chemical
name entries were new chemicals and which were chemical names that were split onto multiple lines. I was then able to fix chemical names appropriately. There were a letters where the start_cas wasn't in the same line as the first chemical starting with a certain letter. Those are
taken care of in dif_start.
"""

c=0 #counter for chemical names that are in dif_start. used to make sure the correct letter is paired with the correct start/stop

for i in range(len(letter_range)): #sets loop to read the file once for each letter
    start=False #used to start parsing and saving information for each letter
    add_on=False #used to indicate when a chemical name or func use is on multiple lines and the lines after the first need to be added to the previous chemical entry
    cas_flag_4=False #used to indicate if a cas number is present in the line

    ifile=open(text_file, encoding='cp1252')
    for line in ifile:
        if line=='\n': continue
        cline=clean(line)
        cline=cline.lower()
        cline=cline.replace(';',',')
        cline=cline.strip()
        cline=cline.split(" ")
        cline = [x.strip() for x in cline if x != ""]

        #sets the start flag to True if there is a cas number in the line that is in the letter_range list and the line starts with the corresponding letter from the list or if the first word is in dif_start and starts with the appropriate letter.
        if (letter_range[i][1] in cline and cline[0][0]==letter_range[i][0]) or cline[0] in dif_start:
            letter=letter_range[i][0]
            if letter_range[i][1] in cline and cline[0][0]==letter_range[i][0]:
                start=True
            else:
                try:
                    if cline[0]==dif_start[c] and dif_start[c][0]==letter:
                        start=True
                        c+=1
                except:
                    continue


        if start==True:
            if cline[0][0]==letter and cline[0] not in use_keys:#if the first letter of the line is "correct" for the iteration of the loop and the first word isn't indicative of a functional use, then this is likely, but not always, a new chemical name.
                cas_flag_4=False #assume no cas in line
                add_on=False #assume this is the first entry of a chemical
                for word in cline:#check for a cas in the line and if there is one, save its location and flip cas_flag_4 to True to indicate a cas is present
                    if bool(cas_pattern.match(word)) or word=="na":
                        cas_index=cline.index(word)
                        cas_flag_4=True
                        break
                if cas_flag_4==True:
                    if add_on==False:#if a cas is in the line and this is the first entry for the chemical add the name, cas, and functional use to the corresponding list. Flip add_on to True so if the chemical name is split, we know to add the next line on to this one
                        raw_chem_name.append(" ".join(cline[:cas_index]))
                        raw_cas.append(cline[cas_index])
                        reported_funcuse.append(" ".join(cline[cas_index+1:]))
                        add_on=True
                    else:#if a cas is in the line but this is not the first entry for the chemical, add the chemical name on to the last entry in the list and make the previous cas and functional use the current cas and functional use. Flip add_on back to False so we start a new entry
                        raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline[:cas_index])
                        raw_cas[-1]=cline[cas_index]
                        reported_funcuse[-1]=reported_funcuse[-1]+" "+" ".join(cline[cas_index+1:])
                        add_on=False
                else:
                    if add_on==False and cline[0]!="anhydride":#If a cas is not in the line but this is the first entry for a chemical, add the chemical name to the name list and empty strings to the cas and functional use lists to preserve length. Flip add_on to True so if the chemical name is split we know to add the next line on to this one. Anhydride was special one-off case that needed to be omitted from this condition. It is taken care of in the "else" below
                        raw_chem_name.append(" ".join(cline))
                        raw_cas.append("")
                        reported_funcuse.append("")
                        add_on=True
                    else:#if a cas is not in the line, add the chemical name on to the previous entry in the list. Flip add_on back to False so we start a new entry.
                        raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline)
                        add_on=False

            elif cline[0] in use_keys:#if the first word in the line is in use_keys check if the word is "fragrance" or "solvent" since there are a handful of chemicals that start with those words. Deal with those cases accordingly then for all other cases edit the previous functional use entry.
                if cline[0]=="solvent" and len(cline)>3:
                    for word in cline:
                        if bool(cas_pattern.match(word)) or word=="na":
                            cas_index=cline.index(word)
                            break
                    raw_chem_name.append(" ".join(cline[:cas_index]))
                    raw_cas.append(cline[cas_index])
                    reported_funcuse.append(" ".join(cline[cas_index+1:]))
                    add_on=True
                elif cline[0]=="fragrance" and cline[-1]=="fragrance":
                    raw_chem_name.append(" ".join(cline[:cline.index("na")]))
                    raw_cas.append(cline[cline.index("na")])
                    reported_funcuse.append(cline[-1])
                    add_on=True
                else:
                    reported_funcuse[-1]=reported_funcuse[-1]+" "+" ".join(cline)

            elif cline[0][0] in alphabet or cline[0][0].isdigit() or cline[0][0] in symbols:#if the first letter of the line is not the letter of focus, a symbol, or numeric, then this is part of a split chemical name. Check for a cas then edit the previous entry
                cas_flag_4=False#assume no cas in line
                for word in cline:#check for a cas in the line and if there is one, save its location and flip cas_flag_4 to True to indicate a cas is present
                    if bool(cas_pattern.match(word)) or word=="na":
                        cas_index=cline.index(word)
                        cas_flag_4=True
                        break
                if cline[0]=="whole":#odd special case
                    break
                else:
                    if cas_flag_4==True:#if there is a cas in the line then add the chemical name and functional uses on to the previous entries and make the previous cas the current cas
                        raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline[:cas_index])
                        raw_cas[-1]=cline[cas_index]
                        reported_funcuse[-1]=reported_funcuse[-1]+" "+" ".join(cline[cas_index+1:])
                    else:
                        if cline[-1] in use_keys:#if there is not a cas in the line and the last word of the line is a fnctional use, then add the chemical name to the previous entry in the chemical and add the functional use to the previous functional use
                            raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline[:-1])
                            reported_funcuse[-1]=reported_funcuse[-1]+" "+cline[-1]
                        else:#if the only thing in the line is part of a chemical name, add it to the previous chemical name
                            raw_chem_name[-1]=raw_chem_name[-1]+" "+" ".join(cline)


            if letter_range[i][2] in cline:# stop reading and parsing the file for the letter in the current iteration of the loop if the letter_stop cas is in the line
                start=False
                break

#create a dataframe of the extracted text
df=pd.DataFrame()
df["raw_chem_name"]=raw_chem_name
df["raw_cas"]=raw_cas
df["report_funcuse"]=reported_funcuse

#make minor one-off corrections that would have required annpying additional logic
df.loc[df.raw_cas=="223749-79-9",["raw_chem_name"]]=df.raw_chem_name+" "+"japonica flower extract"
df.loc[df.raw_cas=="68990-67-0",["raw_chem_name"]]=df.raw_chem_name+" "+"wood extract"
df.loc[df.raw_cas=="37251-67-5",["raw_chem_name"]]=df.raw_chem_name+" "+"monodecyl ether"
df.loc[df.raw_cas=="822-12-8",["report_funcuse"]]="surfactant"
df.loc[df.raw_cas=="7631-99-4",["report_funcuse"]]="preservative, bleaching- "+df.report_funcuse
df.loc[df.raw_cas=="68555-36-2",["raw_chem_name"]]=df.raw_chem_name+" "+"with 1,1'-oxybis[2-chloroethane]"

#replace commas w/ semicolon so we can upload multiple funcuses for each chemical to factotum
df.report_funcuse=df.report_funcuse.str.replace(",",";")

df["data_document_id"]="1512907"
df["data_document_filename"]="IngredientSearch_ACI.pdf"
df["doc_date"]="2020"
df["raw_category"]=""
df["cat_code"]=""
df["description_cpcat"]=""
df["cpcat_sourcetype"]=""
df["component"]=""

df=df[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]

df.to_csv("aci_ingredient_inventory.csv", index=False)
