from tabula import read_pdf
import pandas as pd
import string

table=read_pdf("document_1370045.pdf", pages="11-31,33-35", multiple_tables=True, pandas_options={'header': None})

three=[]
four=[]

for i in range(0, len(table)):
    if len(table[i].columns)==3:
        three.append(i)
    elif len(table[i].columns)==4:
        four.append(i)

three_col=[]
for j in three:
    three_col.append(table[j])

four_col=[]
for k in four:
    four_col.append(table[k])

three_tab=pd.concat(three_col, ignore_index=True)
four_tab=pd.concat(four_col, ignore_index=True)


three_tab["raw_chem_name"]=three_tab.iloc[:,0]
three_tab["raw_cas"]=three_tab.iloc[:,2]
three_tab["EC"]=three_tab.iloc[:,1]
three_tab=three_tab.loc[three_tab["raw_cas"]!= "CAS number"]
three_tab=three_tab.reset_index()
three_tab=three_tab[["raw_chem_name","raw_cas","EC"]]

four_tab["raw_chem_name"]=four_tab.iloc[:,0]
four_tab["raw_cas"]=four_tab.iloc[:,3]
four_tab["EC"]=four_tab.iloc[:,2]
four_tab=four_tab.loc[four_tab["raw_cas"]!= "CAS number"]
four_tab=four_tab.reset_index()
four_tab=four_tab[["raw_chem_name","raw_cas","EC"]]

four_indices_to_drop=[]
for l in range(0,len(four_tab)):
    if  pd.isnull(four_tab["EC"].iloc[l])==False:
        good_chem_index=l
    elif pd.isnull(four_tab["raw_cas"].iloc[l]) and pd.isnull(four_tab["EC"].iloc[l]):
        four_tab["raw_chem_name"].iloc[good_chem_index]=four_tab["raw_chem_name"].iloc[good_chem_index]+four_tab["raw_chem_name"].iloc[l]
        four_indices_to_drop.append(l)
    else:
        continue

four_tab=four_tab.drop(four_indices_to_drop)
four_tab=four_tab.reset_index()
four_tab=four_tab[["raw_chem_name","raw_cas"]]

three_indices_to_drop=[]
for m in range(0,len(three_tab)):
    if  pd.isnull(three_tab["EC"].iloc[m])==False:
        good_chem_index_2=m

    elif pd.isnull(three_tab["raw_cas"].iloc[m]) and pd.isnull(three_tab["EC"].iloc[m]):
        three_tab["raw_chem_name"].iloc[good_chem_index_2]=three_tab["raw_chem_name"].iloc[good_chem_index_2]+three_tab["raw_chem_name"].iloc[m]
        three_indices_to_drop.append(m)
    else:
        continue


three_tab=three_tab.drop(three_indices_to_drop)
three_tab=three_tab.reset_index()
three_tab["raw_cas"].iloc[422]=three_tab["raw_cas"].iloc[422]+three_tab["raw_cas"].iloc[423]
temp_s=three_tab["raw_chem_name"].iloc[422].split("]")
x=temp_s[-1]
temp_s[-1]="] "+three_tab["raw_chem_name"].iloc[423]
temp_s.append(x)
three_tab["raw_chem_name"].iloc[422]="".join(temp_s)
three_tab=three_tab.drop(423)
three_tab=three_tab.reset_index()
three_tab=three_tab[["raw_chem_name","raw_cas"]]


p_thr_two=read_pdf("document_1370045.pdf", pages="32", pandas_options={'header': None})
p_thr_two["raw_chem_name"]=p_thr_two.iloc[:,0]
p_thr_two["raw_cas"]=p_thr_two.iloc[:,2]
p_thr_two=p_thr_two.loc[p_thr_two["raw_cas"]!= "CAS number"]
p_thr_two=p_thr_two[["raw_chem_name","raw_cas"]]
p_thr_two=p_thr_two.dropna(how="all")
p_thr_two=p_thr_two.reset_index()
p_thr_two["flagged"]=0
p_thr_two=p_thr_two[["raw_chem_name","raw_cas","flagged"]]

thr_two_to_drop=[]
for n in range(0,len(p_thr_two)):
    if n in [7,8,9,10,11,12]:
        p_thr_two["flagged"].iloc[n]=1

    if p_thr_two["flagged"].iloc[n]==0:
        if pd.isnull(p_thr_two["raw_chem_name"].iloc[n])==False and pd.isnull(p_thr_two["raw_cas"].iloc[n])==False:
            good_chem_index_3=n
        elif pd.isnull(p_thr_two["raw_chem_name"].iloc[n])==False and pd.isnull(p_thr_two["raw_cas"].iloc[n]):
            p_thr_two["raw_chem_name"].iloc[good_chem_index_3]= p_thr_two["raw_chem_name"].iloc[good_chem_index_3]+p_thr_two["raw_chem_name"].iloc[n]
            thr_two_to_drop.append(n)
    else:
        if pd.isnull(p_thr_two["raw_cas"].iloc[n+1])==False:
            p_thr_two["raw_chem_name"].iloc[n-1]= p_thr_two["raw_chem_name"].iloc[n-1]+p_thr_two["raw_chem_name"].iloc[n]
            thr_two_to_drop.append(n)

p_thr_two=p_thr_two.drop(thr_two_to_drop)
p_thr_two=p_thr_two.reset_index()
p_thr_two=p_thr_two[["raw_chem_name","raw_cas"]]


p_thr_six=read_pdf("document_1370045.pdf", pages="36", pandas_options={'header': None})
p_thr_six["raw_chem_name"]=p_thr_six.iloc[:,0]
p_thr_six["raw_cas"]=p_thr_six.iloc[:,2]
p_thr_six=p_thr_six.loc[p_thr_six["raw_cas"]!= "CAS number"]
p_thr_six=p_thr_six.reset_index()
p_thr_six=p_thr_six[["raw_chem_name","raw_cas"]]
p_thr_six["raw_chem_name"].iloc[0]=p_thr_six["raw_chem_name"].iloc[0]+p_thr_six["raw_chem_name"].iloc[1]+p_thr_six["raw_chem_name"].iloc[2]
p_thr_six["raw_chem_name"].iloc[3]=p_thr_six["raw_chem_name"].iloc[3]+p_thr_six["raw_chem_name"].iloc[4]
p_thr_six["raw_chem_name"].iloc[5]=p_thr_six["raw_chem_name"].iloc[5]+p_thr_six["raw_chem_name"].iloc[6]
p_thr_six["raw_chem_name"].iloc[8]=p_thr_six["raw_chem_name"].iloc[8]+p_thr_six["raw_chem_name"].iloc[9]+p_thr_six["raw_chem_name"].iloc[10]
p_thr_six["raw_chem_name"].iloc[11]=p_thr_six["raw_chem_name"].iloc[11]+p_thr_six["raw_chem_name"].iloc[12]+p_thr_six["raw_chem_name"].iloc[13]
p_thr_six["raw_chem_name"].iloc[14]=p_thr_six["raw_chem_name"].iloc[14]+p_thr_six["raw_chem_name"].iloc[15]+p_thr_six["raw_chem_name"].iloc[16]
p_thr_six=p_thr_six.drop([1,2,4,6,9,10,12,13,15,16])


df=pd.concat([three_tab,four_tab,p_thr_two, p_thr_six], ignore_index=True)

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for o in range(0, len(df)):
    df["raw_chem_name"].iloc[o]=clean(str(df["raw_chem_name"].iloc[o]))
    df["raw_chem_name"].iloc[o]=df["raw_chem_name"].iloc[o].replace(",", "_")
    df["raw_chem_name"].iloc[o]=df["raw_chem_name"].iloc[o].strip().lower()

    df["raw_cas"].iloc[o]=clean(str(df["raw_cas"].iloc[o]))
    df["raw_cas"].iloc[o]=df["raw_cas"].iloc[o].replace(",","_")
    df["raw_cas"].iloc[o]=df["raw_cas"].iloc[o].strip().lower()

df=df.drop_duplicates()
df=df.reset_index()
df=df.drop(columns="index")

df["data_document_id"]="1370045"
df["data_document_filename"]="EU_BPD_2007_a.pdf"
df["doc_date"]="4 December 2007"
df["raw_category"]="raw category"
df["cat_code"]="ACToR Assays"
df["description_cpcat"]="cpcat description"
df["cpcat_code"]="cpcat code"
df["cpcat_sourcetype"]="ACToR Assays and Lists"


#writes df to csv
df.to_csv("EU_reg_com_1451.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
