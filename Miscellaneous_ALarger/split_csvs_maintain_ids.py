
import os, math
import pandas as pd

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Mixed/' #Path file is in
f = 'airgas mixed extracted text.csv' #File name to be split

os.chdir(path)

#get the number of lines of the csv file to be read
number_lines = sum(1 for row in (open(f,encoding="utf8")))


rowsize = 10000 #Number of rows you want in each csv (note: actual number may be slightly higher)
nfiles=math.ceil(number_lines/rowsize)

df = pd.read_csv(f,dtype="string")
header=df.columns
i=0
j=0
for index, row in df.iterrows():
    if i == 0:
        df2 = df.iloc[index:index+1,:]
    
    else: df2=pd.concat([df2,df.iloc[index:index+1]])

    if i>rowsize and row[0] != df.iloc[index+1,0]: #and id not the same
        #make csv
        df2.to_csv(f.split('.csv')[0]+'_'+str(j)+'.csv',index=False, header=True)
        j+=1
        i=-1        
    print(index)
    i+=1
    

df2.to_csv(f.split('.csv')[0]+'_'+str(j)+'.csv',index=False, header=True)
    
