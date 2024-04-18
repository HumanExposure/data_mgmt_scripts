import os
import re
import pandas as pd
from tqdm import tqdm

path = r"C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Files"

os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Files')

df_id = pd.read_csv('Factotum_State_Industrial_Products_unextracted_documents_20240410.csv')

def text_to_table(text):
    line_re = re.compile(r'^(.*?)\s{2,}(.*?)\s{2,}(.*?)\s{2,}(.*?)\s{2,}(.*?)$')
    lines = text.split('\n')
    data = []
    current_row = []
    for line in lines:
        # skip lines that only contain whitespace
        if not line.strip():
            continue
        # match the line with the regular expression
        match = line_re.match(line)
        if match:
            # if the current row is not empty, add it to the data
            if current_row:
                data.append(current_row)
            # start a new row with the matched groups
            current_row = list(match.groups())
        else:
            # if the line does not match the regular expression, it is a continuation of the chemical name
            current_row[0] += ' ' + line.strip()  # append the line to the chemical name
    # add the last row to the data
    if current_row:
        data.append(current_row)
    df = pd.DataFrame(data, columns=['raw_chem_name', 'raw_cas', 'raw_central_comp', 'Column4', 'Column5'])
    df = df[df['raw_chem_name'] != 'Hazardous Ingredients']
    df = df[df['raw_chem_name'] != '']
    df.drop(['Column4','Column5'],axis=1,inplace=True)
    print(df)
    return df




def extractData(files):
    """
    Extracts data from text files and writes it to a CSV file
    files: list of filenames
    """
    for file in tqdm(files):
        if os.path.basename(file) == "Make-A-Bond - Case of 4 rolls.txt":
            continue
        print(file)
        with open(file, 'r', encoding='latin1') as f:
            text = f.read()
        # find the start and end of the data
        start = re.search(r"Hazardous Ingredients\s+CAS Number\s+Weight\s+ACGIH\s+OSHA", text)
        end = re.search(r'4\. FIRST AID MEASURES', text)
        # extract the data and convert it to a table
        data_text = text[start.end():end.start()]
        df = text_to_table(data_text)
        # add the data_document_id column
        filename = os.path.splitext(os.path.basename(file))[0] + '.pdf'
        df['data_document_id'] = df_id[df_id['data_document_filename'] == filename]['data_document_id'].values[0]
        # write the DataFrame to a CSV file
        csv_file = os.path.join(os.getcwd(), 'CSV files', os.path.splitext(os.path.basename(file))[0] + '.csv')
        df.to_csv(csv_file, index=False)

text_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.txt')]

extractData(text_files)
