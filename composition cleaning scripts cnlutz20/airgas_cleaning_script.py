


# %%
import csv, os
import re
import pandas as pd
# %%
idList = [] #Product ids
lowerList = [] #Document title
centList = [] #Document type
upperList = [] #Product page urls

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Cleaning Scripts\Airgas Hardgoods")
file = 'comp_records.csv' #Name of raw extracted records file
newName = file.replace('.csv', '_cleaned')
# %%
template = csv.reader(open(file))


not_percent = []
other = []
for row in template:
    # if row[4]==row[5]==row[6]==row[7]=='': continue
    # print(row)
    
    if row[4] == row[6] and row[5] == '': #Same number in min and max, move concentration to central
        row[5] = row[4]
        row[4] = ''
        row[6] = ''
    if row[7] == 'percent':
        
        #Split up ranges
        if row[5].count('-') == 1:
            row[4] = row[5].split('-')[0].strip()
            row[6] = row[5].split('-')[1].strip()
            row[5] = ''
        if '<' in row[5] and row[4]=='' and row[6]=='':
        # if ('<' in row[5] or '≤' in row[5] or 'min' in row[5]) and row[4]=='' and row[6]=='':
            row[4] = '0'
            row[6] = row[5].strip('< ')
            row[5] = ''
        elif 'min' in row[5] and row[4]=='' and row[6]=='':
            row[6] = '100'
            row[4] = re.findall(r'\d+\.\d+', row[5])[0]
            row[5] = ''

        
        elif ('>' in row[5] or 'max' in row[5] or '≤' in row[5]) and row[4]=='' and row[6]=='':
            if '≤' in row[5]:
                row[6] = row[5].strip('≤')
                row[4] = '0'
                row[5] = ''
            elif 'max' in row[5]:
                row[6] = row[5].split(' ',1)[0].strip()
                row[5] = ''
                row[4] = '0'

            else:    
                row[6] = '100'
                row[4] = row[5].strip('> ')
                row[5] = ''
                
        #Get rid of extra symbols
        row[4] = row[4].replace('bal.', '').replace('<1','0').strip().strip(' >')
        row[5] = row[5].strip('=% ')
        row[6] = row[6].strip('<=% ')

        if re.search(r'\d,\d', row[4]): 
            row[4] = row[4].replace(',', '.')
        if re.search(r'\d,\d', row[5]): 
            row[5] = row[5].replace(',', '.')
        if re.search(r'\d,\d', row[6]): 
            row[6] = row[6].replace(',', '.')
        
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

        else: 
            # continue
            print('########other#########')
            print(row[0]) #Print rows not being cleaned
            other.append(row)
            print('\n')
    else:
            # continue
            print('#######not a percent#########')
            print(row[0]) #Print rows not being cleaned
            not_percent.append(row)
            print('\n')

# %%
df = pd.DataFrame({'ExtractedComposition_id':idList, 'lower_wf_analysis':lowerList, 'central_wf_analysis':centList, 'upper_wf_analysis':upperList})

# %%
df.to_csv(str(newName) + '.csv',index=False, header=True)


# %%
