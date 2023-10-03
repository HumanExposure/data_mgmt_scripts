
import os
import pandas as pd
import numpy as np
import re
import string

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

def harmonize_statname(rawname,rawtype,value,data_document_id):
    note = ''
    rawtype=rawtype.lower().replace(' ','')
    name = rawname.lower().replace(' ','').replace('_','').replace('.','')
    name = name.replace('minimum','min').replace('maximum','max').replace('geometric','geo').replace('average','mean').replace('(','').replace(')','').replace('-','')
    if 'low' in name and name != 'low' and 'est' not in name:
    #     name=name.replace('low','')
        note=rawname
    if 'high' in name and name != 'high' and 'est' not in name:
    #     name=name.replace('high','')
        note=rawname
    if '12hour' in name:
        name=name.replace('12hour','')
        note = rawname
    if '24hour' in name:
        name=name.replace('24hour','')
        note = rawname
    notewords = ['school','home','car','office','indoor','public','kinder','site','zone','air','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','200','199','men']
    if any(x in name for x in notewords): 
        note = rawname
        
    if rawtype == 'percentile': 
        nums = re.findall(r'\d+', rawname)
        if 'ci' in name and ('low' in name or 'high' in name): name = 'SKIP'
        elif len(nums) != 1: 
            if name == 'iqr': name = 'IQR'
            elif name == 'geo': name = 'GEO_MEAN'
            elif name == 'median': name = 'MEDIAN'
            elif name == 'maxconcentration': name = 'MAX'
            elif name == 'meanconcentration': name = 'MEAN'
            else: print(nums,rawname,name,rawtype,value,data_document_id)
        elif nums[0] == '1': 
            if 'q' in name: name ='P25'
            else:name = 'P1'
        elif nums[0] == '2' and 'q' in name: name = 'P50'
        elif nums[0] == '3' and 'q' in name: name = 'P75'
        elif nums[0] == '5': name = 'P5'
        elif nums[0] == '9': name = 'P9'
        elif nums[0] == '10': name = 'P10'
        elif nums[0] == '25': name = 'P25'
        elif nums[0] == '50': name = 'P50'
        elif nums[0] == '75': name = 'P75'
        elif nums[0] == '90': name = 'P90'
        elif nums[0] == '95': name = 'P95'
        elif nums[0] == '98': name = 'P98'
        elif nums[0] == '99': name = 'P99'
        elif nums[0] == '100': name = 'MAX'
        else: print(nums,rawname,name,rawtype,value,data_document_id)
        
    elif rawtype == 'arithmeticmean':
        if name.replace('arithmetic','').replace('mean','').replace('average','').replace('concentration','') == '': name = 'MEAN'
        elif 'geo' in name or 'gemoetric' in name: name = 'GEO_MEAN'
        elif 'sd' in name or 'standarddeviation' in name: name = 'SD'
        elif 'median' in name:
            name='MEDIAN'
        elif 'low' in name:
            note = rawname
            name='MEAN'
        elif 'high' in name:
            note = rawname
            name='MEAN'
        elif name == 'p95' or name == '95thpercentile': name = 'P95'
        elif name == 'p5' or name == '5thpercentile': name = 'P5'
        elif name == 'minmean':
            name = 'MEAN'
            note = rawname
        elif 'min' in name: name = 'MIN'
        elif name == 'maxmean': 
            name = 'MEAN'
            note = rawname
        elif 'max' in name: name = 'MAX'
        elif 'singlevalue' in name:
            name = 'MEAN'
            note = rawname
        else: 
            name = 'MEAN'
        
    elif rawtype == 'geometricmean':
        if name.replace('geo','').replace('mean','').replace('average','').replace('concentration','').replace('total','').replace('gm','') == '': name = 'GEO_MEAN'
        elif 'low' in name:
            note = rawname
            name='GEO_MEAN'
        elif 'high' in name:
            note = rawname
            name='GEO_MEAN'
        elif 'standarddeviation' in name: 
            name = 'GSD'
        else: 
            note = rawname
            name='GEO_MEAN'
            
    elif rawtype == 'median':
        if name == 'median': name = 'MEDIAN'
        elif 'low' in name:
            note = rawname
            name='MEDIAN'
        elif 'high' in name:
            note = rawname
            name='MEDIAN'
        elif name == 'p25' or name == '25thpercentile': name = 'P25'
        elif name == 'p50' or name == '50thpercentile' or name == '50th': name = 'P50'
        elif name == 'p75' or name == '75thpercentile': name = 'P75'
        elif name == 'p95' or name == '95thpercentile': name = 'P95'
        elif 'sd' in name or 'standarddeviation' in name: name = 'SD'
        elif name == 'minmedian':
            name = 'MEDIAN'
            note = rawname
        elif 'min' in name: name = 'MIN'
        elif name == 'maxmedian': 
            name = 'MEDIAN'
            note = rawname
        elif 'max' in name: name = 'MAX'
        elif name == 'geomean': name='GEO_MEAN'
        else: 
            name = 'MEDIAN'
            
    elif rawtype == 'min': 
        if name.replace('min','').replace('detected','').replace('concentration','').replace('range','').replace('lowest','') == '': name = 'MIN'
        elif 'max' in name: name = 'MAX'
        elif 'high' in name: 
            name = 'MIN'
            note = rawname
        else: 
            name = 'MIN'
        
    elif rawtype == 'max':
        if name.replace('max','').replace('detected','').replace('concentration','').replace('range','').replace('highest','') == '': name = 'MAX'
        elif 'min' in name or 'high' in name or 'median' in name or 'low' in name or 'mean' in name:
            name = 'MAX'
            note = rawname
        else: 
            name = 'MAX'
        
    elif rawtype == 'std.deviation':
        if name.replace('std','').replace('deviation','').replace('standard','').replace('sd','') == '': name = 'SD'
        elif 'geo' in name: name='GSD'
        elif 'standarderror' in name: name = 'SE'
        elif name == 'min': name='MIN'
        elif name == 'median': name='MEDIAN'
        elif name == 'max': name = 'MAX'
        elif 'confidenceinterval' in name: name = 'SKIP'
        else: 
            name = 'SD'
        if name == 'SD':
            if 'low' in name: note=rawname
            if 'high' in name: note=rawname
            if 'median'in name: note=rawname
            if 'mean' in name: note=rawname
            if '#' in name: note=rawname
            
    elif rawtype == 'variance':
        if 'SE' in rawname.split(' ') or name=='public' or name=='homemedian': name = 'SE'
        elif 'standarddeviation' in name: name = 'SD'
        elif name == 'coefficientofvariation': name = 'CV'
        else:
            print(rawname,name,rawtype,value,data_document_id)
        
    elif rawtype == 'gsd':
        if name == 'geostandarddeviation': name = 'GSD'
        elif name == 'mean': name = 'MEAN' 
        else:
            print(rawname,name,rawtype,value,data_document_id)
        
    else: print(rawtype)
    
    if any(x not in '1234567890.' for x in value): 
        print(rawname,name,rawtype,value,data_document_id)
        note = (note+', value='+value).strip(', ')
        value = 'None'
        # name='SKIP'
        # print(rawname,name,rawtype,value,data_document_id)
    
    return name, note, value

def harmonize_media(medium):
    harmonized_medium = medium.lower().strip()
    if harmonized_medium == 'airborne particulate matter from building hvac system': harmonized_medium = 'indoor dust'
    elif harmonized_medium == 'amphipods': harmonized_medium =  'wildlife (aquatic invertebrate)'
    elif harmonized_medium == 'blood': harmonized_medium = 'human blood (whole/serum/plasma)'
    elif harmonized_medium == 'cat food': harmonized_medium = 'product'
    elif harmonized_medium == 'cat serum': harmonized_medium = 'wildlife (terrestrial vertebrates)'
    elif harmonized_medium == 'circuit board': harmonized_medium = 'product'
    elif harmonized_medium == 'clothes lint': harmonized_medium = 'product'
    elif harmonized_medium == 'dust inside TV': harmonized_medium = 'indoor dust'
    elif harmonized_medium == 'exhaled breath': harmonized_medium = 'personal air'
    elif harmonized_medium == 'feces': harmonized_medium = 'human (other tissues or fluids)'
    elif harmonized_medium == 'fish tissue': harmonized_medium = 'wildlife (fish)'
    elif harmonized_medium == 'foam': harmonized_medium = 'product'
    elif harmonized_medium == 'food': harmonized_medium = 'food product'
    elif harmonized_medium == 'food products': harmonized_medium = 'food product'
    elif harmonized_medium == 'front cabinet': harmonized_medium = 'product'
    elif harmonized_medium == 'hair': harmonized_medium = 'human (other tissues or fluids)'
    elif harmonized_medium == 'indoor air + outdoor air': harmonized_medium = 'ambient air'
    elif harmonized_medium == 'lichen': harmonized_medium = 'other-ecological'
    elif harmonized_medium == 'moss': harmonized_medium = 'vegetation'  
    elif harmonized_medium == 'outdoor surface dust': harmonized_medium = 'soil'
    elif harmonized_medium == 'phytoplankton': harmonized_medium = 'other-ecological'
    elif harmonized_medium == 'pooled dairy milk': harmonized_medium = 'food product'
    elif harmonized_medium == 'rear cabinet': harmonized_medium = 'product'
    elif harmonized_medium == 'serum': harmonized_medium = 'human blood (whole/serum/plasma)'
    elif harmonized_medium == 'sewage sludge': harmonized_medium = 'sludge'
    elif harmonized_medium == 'treated wastewater': harmonized_medium = 'wastewater (influent, effluent)'
    elif harmonized_medium == 'dust inside tv': harmonized_medium = 'indoor dust'
    elif harmonized_medium == 'surface wipes': harmonized_medium = 'indoor dust'
    # else: print(harmonized_medium)
    return harmonized_medium

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Indoor Air and Dust/Upload'
os.chdir(path)

#read files with data
dft = pd.read_csv('Factotum_Indoor_Air_and_Dust_unextracted_documents_20230411.csv') #Upload template
header = list(dft.columns)
df1 = pd.read_excel('IAD_Phase1_data052518.xlsx', sheet_name='flexible_form_results').replace(np.nan,'',regex=True) #phase 1 data
df2 = pd.read_csv('TO-024_IAD_Phase2 Data_103020.csv').replace(np.nan,'',regex=True) #Phase 2 indoor air and dust data
dfb = pd.read_excel('NCCT_TO-14_Phase 2 Biomonitoring Data_28July2021.xlsx', sheet_name='Phase 2 Biomonitoring Results').replace(np.nan,'',regex=True) #phase 2 biomonitoring results


# allNames = []

df = pd.DataFrame(columns = header)

for index, row in dft.iterrows() :
    # print(row['data_document_id'], row['data_document_filename'])
    # print(index)

    

    #List of chems from phase 1    
    phase1chems = []
    phase1cas = []
    
    #List of chems from phase 2
    phase2chems = []
    phase2cas = []


    """
    Get data on study
    """
    #Extracted text fields
    data_document_id = ''
    data_document_filename = ''	
    doc_date = ''
    study_type = ''	
    media = ''
    qa_flag = ''
    qa_who = ''
    extraction_wa = ''
    

    #Get factotum ID, filename, and hero ID
    data_document_id = row['data_document_id']
    data_document_filename = row['data_document_filename']
    heroID = int(data_document_filename.split('.')[0].split('_')[0])
    # print(heroID)
    
    
    #Get phase 1 data
    data = df1.loc[df1['study heroId'] == heroID]
    for index2, row2 in data.iterrows():
        if str(row2['studyPopulations.Medium.matrix']) != 'nan' and str(row2['studyPopulations.Medium.matrix']) not in media:
            media = (media + ', ' + row2['studyPopulations.Medium.matrix']).strip(', ')
        # phase1cas.append(row2['studyPopulations.Medium.Chemistry.casNumber'])
        # phase1chems.append(['studyPopulations.Medium.Chemistry.chemicalName'])
        # print(media)
        if 'Phase 1:' not in extraction_wa:
            extraction_wa = (extraction_wa+ ', '+'Phase 1: ICF WA4-108 2018').strip(', ')

    #Get indoor air and dust data
    data = df2.loc[df2['studyHeroId'] == heroID]
    for index2, row2 in data.iterrows():
        if str(row2['flexData:studyPopulations:Medium:matrix']) not in media:
            media = (media + ', ' + row2['flexData:studyPopulations:Medium:matrix']).strip(', ')
        if doc_date == '': doc_date = row2['year']
        if row2['flexData:studyPopulations:Medium:methodType'] == 'Targeted':
            study_type = 'Targeted'
        elif row2['flexData:studyPopulations:Medium:methodType'] == 'Screening':
            study_type = 'Non-Targeted'
        if 'Indoor air and dust:' not in qa_flag and row2['QC Status'] != '':
            qa_flag = (qa_flag+', '+'Indoor air and dust: ' + row2['QC Status']).strip(', ')
            qa_who = 'ICF'
        if 'Phase 2 indoor air and dust:' not in extraction_wa:
            extraction_wa = (extraction_wa+ ', '+'Phase 2 indoor air and dust: ICF TO-24 2020').strip(', ')

    
    #Get biomonitoring data
    data = dfb.loc[dfb['studyHeroId'] == heroID]
    for index2, row2 in data.iterrows():
        if str(row2['flexData:studyPopulations:Medium:matrix']) != 'nan' and str(row2['flexData:studyPopulations:Medium:matrix']) not in media:
            media = (media + ', ' + row2['flexData:studyPopulations:Medium:matrix']).strip(', ')
        if doc_date == '': doc_date = row2['year']
        if row2['flexData:studyPopulations:Medium:methodType'] == 'Targeted':
            study_type = 'Targeted'
        elif row2['flexData:studyPopulations:Medium:methodType'] == 'Screening':
            study_type = 'Non-Targeted'
        # if 'Biomonitoring:' not in qa_flag:
            # qa_flag = (qa_flag+', '+'Biomonitoring: ' + row2['QC Status']).strip(', ')
            # qa_who = 'ICF'
        if 'Phase 2 biomonitoring:' not in extraction_wa:
            extraction_wa = (extraction_wa+ ', '+'Phase 2 biomonitoring: ICF TO-14 2022').strip(', ')


    

    """
    Get data on chemicals
    """
    

    #Get indoor air and dust data
    data = df2.loc[df2['studyHeroId'] == heroID]
    for index2, row2 in data.iterrows():
        #Chemical record fields
        raw_chem_name = ''
        raw_cas = ''
        chem_detected_flag = ''
        study_location = ''
        sampling_date = ''
        population_description = ''
        population_gender = ''
        population_age = ''
        population_other = ''
        sampling_method = ''
        analytical_method = ''
        medium = ''
        harmonized_medium = ''
        num_measure = ''
        num_nondetect = ''
        detect_freq = ''
        detect_freq_type = ''
        statistical_values= ''
        #Fields under statistical values
        name = ''
        rawname = ''
        rawtype = ''
        value = ''
        value_type = ''
        stat_unit = ''
        stat_note = ''
    
      
        
        raw_cas = str(row2['flexData:studyPopulations:Medium:Chemistry:casNumber'])
        if raw_cas.lower() == 'nr': raw_cas = ''
        phase2cas.append(raw_cas)
        raw_chem_name = row2['flexData:studyPopulations:Medium:Chemistry:chemicalName']
        phase2chems.append(raw_chem_name.lower())
        if row2['flexData:studyPopulations:Medium:Chemistry:chemicalShort'] not in ['',raw_chem_name]:
            raw_chem_name = raw_chem_name + ' (' + row2['flexData:studyPopulations:Medium:Chemistry:chemicalShort'] + ')'
            phase2chems.append(row2['flexData:studyPopulations:Medium:Chemistry:chemicalShort'].lower())
        medium = row2['flexData:studyPopulations:Medium:matrix']
        if medium == 'other': medium = row2['flexData:studyPopulations:Medium:matrixother']
        
        #Harmonize media
        harmonized_medium = harmonize_media(medium)
        
        
        num_measure = str(row2['flexData:studyPopulations:Medium:Chemistry:totalObservationsReported'])
        if num_measure!=''  and float(num_measure).is_integer() == False:
            print(data_document_id,num_measure)
            num_measure = ''
        detect_freq = str(row2['flexData:studyPopulations:Medium:Chemistry:detectFreq'])
        detect_freq_type = str(row2['flexData:studyPopulations:Medium:Chemistry:dfReported'])
        if detect_freq_type == 'ICF Calculated': detect_freq_type = 'C'
        elif detect_freq_type == 'Study Reported': detect_freq_type = 'R'
        if detect_freq == 'ND': detect_freq='0'
        if all(x in '1234567890.% ' for x in detect_freq) == False: detect_freq = ''
        elif detect_freq != '' and float(detect_freq.strip('% ')) > 0:
            chem_detected_flag = '1'
        elif detect_freq.strip('% ')=='0': 
            chem_detected_flag = '0'
            
        #Some detection frequencies are percents, some are decimals. Change to decimals, and if it isn't clear, leave blank
        if detect_freq != '': 
            if '%' in detect_freq: detect_freq = str(float(detect_freq.strip('% '))/100)
            elif detect_freq == '0': pass #don't change non-detects
            elif float(detect_freq)>1: detect_freq = str(float(detect_freq)/100)
            elif float(detect_freq)<=1 and (num_measure == '' or float(num_measure)>=100): detect_freq = ''
            
        qa_flag = 'Indoor air and dust: ' + row2['QC Status']
        study_location = (str(row2['flexData:studyPopulations:country'])+', '+str(row2['flexData:studyPopulations:locationDetails'])+', '+str(row2['flexData:studyPopulations:locationType'])).strip(', ')
        sampling_date = str(row2['flexData:studyPopulations:Medium:samplingDateRange'])
        population_description = row2['flexData:studyPopulations:populationName']
        sampling_method = row2['flexData:studyPopulations:Medium:samplingNotes']
        if len(sampling_method) > 1000: sampling_method=sampling_method[:999]
        analytical_method = row2['flexData:studyPopulations:Medium:instrumentType']
        
        rawname = row2['flexData:studyPopulations:Medium:Chemistry:statistics:statName'].upper().replace('_',' ').replace('  ',' ').strip()
        rawtype = row2['flexData:studyPopulations:Medium:Chemistry:statistics:statType'].upper().replace('_',' ').replace('  ',' ').strip()
        # allNames.append(name)
        value = str(row2['flexData:studyPopulations:Medium:Chemistry:statistics:statEst'])
        if row2['flexData:studyPopulations:Medium:Chemistry:statistics:statCalc'] == 'Study Reported':
            value_type = "'R'"
        else: value_type = "'C'"
        stat_unit = row2['flexData:studyPopulations:Medium:Chemistry:statistics:statUnit']
        if stat_unit == '': stat_unit = 'None'
        
        if len(df)>0 and df.iloc[-1]['raw_chem_name'] == raw_chem_name and df.iloc[-1]['raw_cas'] == raw_cas and df.iloc[-1]['medium'] == medium:
            #Same chem, new data
            # print('same')
            if rawname != '':
                name,stat_note,value= harmonize_statname(rawname,rawtype,value,data_document_id)
                if name=='SKIP': continue
                df.loc[df.index[-1], 'statistical_values'] = df.loc[df.index[-1], 'statistical_values'] + "; {'name': '"+name+"', 'value': "+value+", 'value_type': "+value_type+", 'stat_unit': '"+stat_unit+"', 'stat_note': '"+stat_note+"'}"

        else:
            #New chem
            if rawname != '':
                name,stat_note,value= harmonize_statname(rawname,rawtype,value,data_document_id)
                if name=='SKIP': continue
                statistical_values = "{'name': '"+name+"', 'value': "+value+", 'value_type': "+value_type+", 'stat_unit': '"+stat_unit+"', 'stat_note': '"+stat_note+"'}"
        
            df = df.append({'data_document_id':data_document_id,'data_document_filename':data_document_filename,'doc_date':clean(str(doc_date)),'study_type':clean(str(study_type)),'media':clean(str(media)),'qa_flag':clean(str(qa_flag)),'qa_who':clean(str(qa_who)),'extraction_wa':clean(str(extraction_wa)),'raw_chem_name':clean(str(raw_chem_name)),'raw_cas':clean(str(raw_cas)),'chem_detected_flag':str(chem_detected_flag).split('.')[0],'study_location':clean(str(study_location)),'sampling_date':clean(str(sampling_date)),'population_description':clean(str(population_description)),'population_gender':clean(str(population_gender)),'population_age':clean(str(population_age)),'population_other':clean(str(population_other)),'sampling_method':clean(str(sampling_method)),'analytical_method':clean(str(analytical_method)),'medium':clean(str(medium)),'harmonized_medium':clean(str(harmonized_medium)),'num_measure':num_measure,'num_nondetect':num_nondetect,'detect_freq':detect_freq,'detect_freq_type':clean(str(detect_freq_type)),'statistical_values':statistical_values},ignore_index=True)

    
    #Get biomonitoring data
    data = dfb.loc[dfb['studyHeroId'] == heroID]
    for index2, row2 in data.iterrows():
        #Chemical record fields
        raw_chem_name = ''
        raw_cas = ''
        chem_detected_flag = ''
        study_location = ''
        sampling_date = ''
        population_description = ''
        population_gender = ''
        population_age = ''
        population_other = ''
        sampling_method = ''
        analytical_method = ''
        medium = ''
        harmonized_medium = ''
        num_measure = ''
        num_nondetect = ''
        detect_freq = ''
        detect_freq_type = ''
        statistical_values= ''
        #Fields under statistical values
        name = ''
        rawname = ''
        rawtype = ''
        value = ''
        value_type = ''
        stat_unit = ''
        stat_note = ''
       
    
        raw_cas = str(row2['flexData:studyPopulations:Medium:Chemistry:casNumber'])
        if raw_cas.lower() == 'nr': raw_cas = ''
        phase2cas.append(raw_cas)
        raw_chem_name = row2['flexData:studyPopulations:Medium:Chemistry:chemicalName']
        phase2chems.append(raw_chem_name.lower())
        if row2['flexData:studyPopulations:Medium:Chemistry:chemicalShort'] not in ['',raw_chem_name]:
            raw_chem_name = raw_chem_name + ' (' + row2['flexData:studyPopulations:Medium:Chemistry:chemicalShort'] + ')'
            phase2chems.append(row2['flexData:studyPopulations:Medium:Chemistry:chemicalShort'].lower())
        medium = row2['flexData:studyPopulations:Medium:matrix']
        if medium == 'other': medium = row2['flexData:studyPopulations:Medium:matrixother']
        
        #Harmonize media
        harmonized_medium = harmonize_media(medium)
       
        
        num_measure = str(row2['flexData:studyPopulations:Medium:Chemistry:totalObservationsReported'])
        if num_measure!=''  and float(num_measure).is_integer() == False:
            print(data_document_id,num_measure)
            num_measure = ''
        detect_freq = str(row2['flexData:studyPopulations:Medium:Chemistry:detectFreq'])
        if detect_freq == 'ND': detect_freq='0'
        if detect_freq_type == 'ICF Calculated': detect_freq_type = 'C'
        elif detect_freq_type == 'Study Reported': detect_freq_type = 'R'
        
        if all(x in '1234567890.' for x in detect_freq) == False: detect_freq = ''
        elif detect_freq != '' and float(detect_freq) > 0:
            chem_detected_flag = '1'
        elif detect_freq=='0': 
            chem_detected_flag = '0'
        # qa_flag = 'Indoor air and dust: ' + row2['QC Status']
        study_location = (row2['flexData:studyPopulations:country']+', ' + str(row2['flexData:studyPopulations:locationDetails'])+', '+row2['flexData:studyPopulations:locationType']).strip(', ')
        sampling_date = str(row2['flexData:studyPopulations:Medium:samplingDateRange'])
        population_description = row2['flexData:studyPopulations:populationName']
        sampling_method = row2['flexData:studyPopulations:Medium:samplingNotes']
        if len(sampling_method) > 1000: sampling_method=sampling_method[:999]
        analytical_method = row2['flexData:studyPopulations:Medium:instrumentType']
            
        rawname = row2['flexData:studyPopulations:Medium:Chemistry:statistics:statName'].upper().replace('_',' ').replace('  ',' ').strip()
        rawtype = row2['flexData:studyPopulations:Medium:Chemistry:statistics:statType'].upper().replace('_',' ').replace('  ',' ').strip()
        # allNames.append(name)
        value = str(row2['flexData:studyPopulations:Medium:Chemistry:statistics:statEst'])
        if row2['flexData:studyPopulations:Medium:Chemistry:statistics:statCalc'] == 'Study Reported':
            value_type = "'R'"
        else: value_type = "'C'"
        stat_unit = row2['flexData:studyPopulations:Medium:Chemistry:statistics:statUnit']
        if stat_unit == '': stat_unit = 'None'
            
        if len(df)>0 and df.iloc[-1]['raw_chem_name'] == raw_chem_name and df.iloc[-1]['raw_cas'] == raw_cas and df.iloc[-1]['medium'] == medium:
            #Same chem, new data
            # print('same')
            if rawname != '':
                name,stat_note,value= harmonize_statname(rawname,rawtype,value,data_document_id)
                if name=='SKIP': continue
                df.loc[df.index[-1], 'statistical_values'] = df.loc[df.index[-1], 'statistical_values'] + "; {'name': '"+name+"', 'value': "+value+", 'value_type': "+value_type+", 'stat_unit': '"+stat_unit+"', 'stat_note': '"+stat_note+"'}"

        else:
            #New chem
            if rawname != '':
                name,stat_note,value= harmonize_statname(rawname,rawtype,value,data_document_id)
                if name=='SKIP': continue
                statistical_values = "{'name': '"+name+"', 'value': "+value+", 'value_type': "+value_type+", 'stat_unit': '"+stat_unit+"', 'stat_note': '"+stat_note+"'}"
            
            df = df.append({'data_document_id':data_document_id,'data_document_filename':data_document_filename,'doc_date':clean(str(doc_date)),'study_type':clean(str(study_type)),'media':clean(str(media)),'qa_flag':clean(str(qa_flag)),'qa_who':clean(str(qa_who)),'extraction_wa':clean(str(extraction_wa)),'raw_chem_name':clean(str(raw_chem_name)),'raw_cas':clean(str(raw_cas)),'chem_detected_flag':str(chem_detected_flag).split('.')[0],'study_location':clean(str(study_location)),'sampling_date':clean(str(sampling_date)),'population_description':clean(str(population_description)),'population_gender':clean(str(population_gender)),'population_age':clean(str(population_age)),'population_other':clean(str(population_other)),'sampling_method':clean(str(sampling_method)),'analytical_method':clean(str(analytical_method)),'medium':clean(str(medium)),'harmonized_medium':clean(str(harmonized_medium)),'num_measure':num_measure,'num_nondetect':num_nondetect,'detect_freq':detect_freq,'detect_freq_type':clean(str(detect_freq_type)),'statistical_values':statistical_values},ignore_index=True)


    #Get phase 1 data
    data = df1.loc[df1['study heroId'] == heroID]
    for index2, row2 in data.iterrows():
        #Chemical record fields
        raw_chem_name = ''
        raw_cas = ''
        chem_detected_flag = ''
        study_location = ''
        sampling_date = ''
        population_description = ''
        population_gender = ''
        population_age = ''
        population_other = ''
        sampling_method = ''
        analytical_method = ''
        medium = ''
        harmonized_medium = ''
        num_measure = ''
        num_nondetect = ''
        detect_freq = ''
        detect_freq_type = ''
        statistical_values= ''
        #Fields under statistical values
        name = ''
        rawname = ''
        rawtype = ''
        value = ''
        value_type = ''
        stat_unit = ''
        stat_note = ''
        
       
        if row2['studyPopulations.Medium.Chemistry.chemicalName'].lower() in phase2chems: continue
        else:
            raw_chem_name = row2['studyPopulations.Medium.Chemistry.chemicalName']
            raw_cas = row2['studyPopulations.Medium.Chemistry.casNumber']
            if raw_cas.lower() == 'nr': raw_cas = ''
            medium = row2['studyPopulations.Medium.matrix']
            if medium == 'other': medium = row2['studyPopulations.Medium.matrixother']
            
            #Harmonize media
            harmonized_medium = harmonize_media(medium)
           
                
           
            study_location = (row2['studyPopulations.country']+', '+str(row2['studyPopulations.locationDetails'])).strip(', ')
            sampling_date = str(row2['studyPopulations.Medium.samplingDateRange'])
            population_description = row2['studyPopulations.populationName']
            
            df = df.append({'data_document_id':data_document_id,'data_document_filename':data_document_filename,'doc_date':clean(str(doc_date)),'study_type':clean(str(study_type)),'media':clean(str(media)),'qa_flag':clean(str(qa_flag)),'qa_who':clean(str(qa_who)),'extraction_wa':clean(str(extraction_wa)),'raw_chem_name':clean(str(raw_chem_name)),'raw_cas':clean(str(raw_cas)),'chem_detected_flag':str(chem_detected_flag).split('.')[0],'study_location':clean(str(study_location)),'sampling_date':clean(str(sampling_date)),'population_description':clean(str(population_description)),'population_gender':clean(str(population_gender)),'population_age':clean(str(population_age)),'population_other':clean(str(population_other)),'sampling_method':clean(str(sampling_method)),'analytical_method':clean(str(analytical_method)),'medium':clean(str(medium)),'harmonized_medium':clean(str(harmonized_medium)),'num_measure':num_measure,'num_nondetect':num_nondetect,'detect_freq':detect_freq,'detect_freq_type':clean(str(detect_freq_type)),'statistical_values':statistical_values},ignore_index=True)

            
       

df.to_csv("indoor air and dust upload 6.csv",index=False,header=True)
