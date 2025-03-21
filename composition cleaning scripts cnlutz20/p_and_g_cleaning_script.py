


# %%
import csv, os
import re
import pandas as pd
# %%
idList = [] #Product ids
lowerList = [] #Document title
centList = [] #Document type
upperList = [] #Product page urls

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Cleaning Scripts\proctor and gamble")
file = 'comp_records.csv' #Name of raw extracted records file
newName = file.replace('.csv', '_cleaned')
# %%
template = csv.reader(open(file))


not_percent = []
other = []
for row in template:
    # if row[4]==row[5]==row[6]==row[7]=='': continue
    # print(row)
    
  
    if all(n in '1234567890., ' for n in row[5]) and row[4] == '' and row[5] != '' and row[6] == '':
        idList.append(row[1])
        lowerList.append('')
        centList.append((pd.to_numeric(row[5])/100).round(10))
        upperList.append('')
        if centList[-1] > 1 or centList[-1] <= 0: #Check if wf makes sense
            print('concentration out of range:',row)
            del idList[-1]
            del lowerList[-1]
            del centList[-1]
            del upperList[-1]

    elif all(n in '1234567890., ' for n in row[4]+row[6]) and row[4] != '' and row[5] == '' and row[6] != '':
        idList.append(row[1])
        lowerList.append((pd.to_numeric(row[4])/100).round(10))
        centList.append('')
        upperList.append((pd.to_numeric(row[6])/100).round(10))
        if any(n > 1 or n < 0 for n in [lowerList[-1],upperList[-1]]) or lowerList[-1] >= upperList[-1]: #Check if wf makes sense
            print('concentration out of range:',row)
            del idList[-1]
            del lowerList[-1]
            del centList[-1]
            del upperList[-1]

    

# %%
df = pd.DataFrame({'ExtractedComposition_id':idList, 'lower_wf_analysis':lowerList, 'central_wf_analysis':centList, 'upper_wf_analysis':upperList})

# %%
df.to_csv(str(newName) + '.csv',index=False, header=True)

