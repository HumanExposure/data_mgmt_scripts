import pandas as pd
from tabula import read_pdf #used to parse pdf into df
import re

master=pd.DataFrame()

#Observed cases of different formatting due to way data was parsed. These should not be considered during string matching
d_bad_format=["d1.492","d1.2","d1.381"]
vp_bad_format=["vp1.7","vp13.4","vp25.3"]

#Tabula couldn't read all the pages at once but can read them individually so extract the table on each page
#then concat everything into one df. Note that the melting point and boiling point for each chemical are initially in the same cell,
#as well as vapor pressure and denisty.These are split into separate columns later on.
for i in range(1,7):
    table=read_pdf("library_refrigerant_ref_table.pdf", pages="%d"%i, lattice=True, pandas_options={'header': None})
    table=table.iloc[3:,[0,2,3,4]] #select data only relevant columns starting from the third row down, which is the first row containg information
    table.columns=["refrigerant_number","cas","mp/bp","vp/d"]
    #create columns to split data for when data is currently in a single column
    table["mp"]=""
    table["bp"]=""
    table["vp"]=""
    table["vp_var"]=""
    table["d"]=""
    table["d_var"]=""
    #for each row in the table extract the refrigerant_number, cas, melting point, boiling point, vapor pressure, and density
    for j in range(len(table)):
        table["refrigerant_number"].iloc[j]="".join(table["refrigerant_number"].iloc[j].split())
        table["cas"].iloc[j]=table["cas"].iloc[j].split()[-1].strip('[').strip(']')
        table["mp"].iloc[j]=table["mp/bp"].iloc[j].split()[0].replace("m.p.","").replace("b","") #melting point is always the first item in the melting/boiling cell
        table["bp"].iloc[j]=table["mp/bp"].iloc[j].split()[-1].replace("b.p.","").replace(".p.","") #boiling point is always last item in the melting/boiling cell
        table["vp/d"].iloc[j]=table["vp/d"].iloc[j].split()
        d_var=[k for k in table["vp/d"].iloc[j] if k.startswith("d")][0] #get the density variable in the vapor pressure/density cell. Since there is variability in the format/temperature getting the value lets me figure out where to splice
        pattern_d=re.compile('d{1}o{0,1}-{0,1}\d{0,2}$|d{1}o{0,1}-{0,1}\d{1,2}\.\d{1,3}$') #regex to match most "d" formats

        #Actually deals with different formatting of "d" values
        if pattern_d.search(d_var) and d_var not in d_bad_format:
            table["d_var"].iloc[j]=pattern_d.findall(d_var)[0]
        else:
            table["d_var"].iloc[j]=False

        if table["d_var"].iloc[j]!=False:
            table["d"].iloc[j]=table["d_var"].iloc[j]+": "+"".join(table["vp/d"].iloc[j][table["vp/d"].iloc[j].index(table["d_var"].iloc[j])+1:])
            if table["d"].iloc[j].strip()=="d:" or table["d"].iloc[j].strip()=="d20:":
                table["d"].iloc[j]=""
        elif table["d_var"].iloc[j]==False and d_var in d_bad_format:
            table["d"].iloc[j]="d: "+"".join(table["vp/d"].iloc[j][table["vp/d"].iloc[j].index(d_var):]).replace("d","")
        else:
            table["d"].iloc[j]="d25: 1.390" #correct another format that isn't picked up by the regex and isn't of the same format as items in d_bad_format

        pattern_vp=re.compile('v\.{0,1}p\.{0,1}$|v\.{0,1}p\.{0,1}-{0,1}\d{1,2}\.{0,1}\d{0,1}$') #regex to match most "vp" formats

        #Actually deals with different formatting of "vp" values
        if pattern_vp.search(table["vp/d"].iloc[j][0]) and table["vp/d"].iloc[j][0] not in vp_bad_format:
            table["vp_var"].iloc[j]=pattern_vp.findall(table["vp/d"].iloc[j][0])[0]
        else:
            table["vp_var"].iloc[j]=False

        if table["vp_var"].iloc[j]!=False:
            table["vp"].iloc[j]=": ".join(table["vp/d"].iloc[j][:table["vp/d"].iloc[j].index(d_var)])
            if table["vp"].iloc[j].endswith("p") or table["vp"].iloc[j].endswith("."):
                table["vp"].iloc[j]=""
        elif table["vp_var"].iloc[j]==False and table["vp/d"].iloc[j][0] in vp_bad_format:
            table["vp"].iloc[j]="vp: "+table["vp/d"].iloc[j][0].replace("vp","")
        else:
            table["vp"].iloc[j]="vp2.5: 14.2" #correct another format that isn't picked up by the regex and isn't of the same format as items in vp_bad_format

    master=pd.concat([master,table], ignore_index=True) #concat all pages together

master=master[["refrigerant_number","cas","mp","bp","vp","d"]]
master.to_csv("pfas_physchem_props.csv", index=False)
