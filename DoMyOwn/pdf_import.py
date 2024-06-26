# -*- coding: utf-8 -*-
"""Read a PDF with Tika/Tessaract and sort it.

Created on Thu Oct 31 17:34:09 2019

@author: SBURNS
"""
import os
import re
import numpy as np
import pandas as pd
from tika import parser
import logging
import requests
import socket
import json
from sqlalchemy import create_engine
from io import BytesIO
import unicodedata


sds = re.compile(r'(?:s\s?d\s?s|d\s?a\s?t\s?a\s{0,3}s\s?h\s?e\s?e\s?t)',
                 re.IGNORECASE)
sds2 = re.compile(r'(?:first.?aid|composition)', re.IGNORECASE)
s3 = re.compile(r'^[\W]{0,8}(?:sectio|chapte)?[rn]?\W{0,2}[^\d]' +
                r'(?:[23]|(?:[i1]{3}|ii))\W{0,8}(?![ ]?\d)[\w\/\& ]*?' +
                r'(?:composition|(?:components|ingredients))', re.IGNORECASE)
s4 = re.compile(r'^[\W]{0,8}(?:sectio|chapte)?[rn]?\W{0,2}[^\d](?:4|iv)' +
                r'\W{0,8}(?![ ]?\d)[\w\/\& ]*?(?:(?:first.?aid)|(?:fire' +
                r'[a-z ]{0,7}explosion))', re.IGNORECASE)
cas1 = re.compile(r'[^\d](?!0\d[\—\–\-\° ]{1,3}[0-3]\d[\—\–\-\° ]{1,3}' +
                  r'(?:[01]\d|20[01]\d))(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})' +
                  r'[\—\–\-\° ]{1,3}([\d])(?!\d{2,})', re.IGNORECASE)
cas12 = re.compile(r'[^\d](?!0\d[\—\–\-\° ]{1,3}[0-3]\d[\—\–\-\° ]{1,3}' +
                   r'(?:[01]\d|20[01]\d))(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})' +
                   r'[\—\–\-\° ]{1,3}[0]([\d])(?!\d{2,})', re.IGNORECASE)
# these are needed to sort out some exceptions
s3_2 = re.compile(r'^[\W]{0,8}(?:sectio|chapte)?[rn]?\W{0,2}[^\d](?:[2]|' +
                  r'(?:ii))\W{0,8}(?![ ]?\d)[\w\/\& ]*?(?:composition|' +
                  r'(?:components|ingredients))', re.IGNORECASE)
s3_3 = re.compile(r'^[\W]{0,8}(?:sectio|chapte)?[rn]?\W{0,2}[^\d](?:[3]|' +
                  r'(?:[i1]{3}))\W{0,8}(?![ ]?\d)[\w\/\& ]*?(?:composition|' +
                  r'(?:components|ingredients))', re.IGNORECASE)


def read_fname_df():
    """Read df of brand name and puc from factotum."""
    with open(r"C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\Scripts\mysql.json", 'r') as f:
        cfg = json.load(f)['mysql']

    # check if db is up (https://stackoverflow.com/questions/17434079)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((cfg['server'], int(cfg['port'])))
    except socket.gaierror:
        logging.warning('Database connection failed')
        df = pd.DataFrame()
    else:
        conn = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                             f'{cfg["password"]}@{cfg["server"]}:' +
                             f'{cfg["port"]}/{cfg["database"]}?charset=utf8',
                             echo=False).connect()
        sql = 'select id, file, filename from dashboard_datadocument;'
        df = pd.read_sql(sql, conn)
        conn.close()
    finally:
        s.close()
    return df


def get_url(fname, fname_list):
    """Get the factotum URL from the filename."""
    url = 'http://factotum.epa.gov/media/' + fname
    r = requests.get(url)
    if r.status_code == 200:
        return r

    if fname_list is None:
        return None

    rdoc = re.search(r'^(?:document_)(\d{4,})[\.](?:pdf)',
                     fname, flags=re.I)
    if rdoc:
        file = fname_list.loc[fname_list['id'] == int(rdoc.group(1)),
                              'file']
        if len(file) == 1:
            url = 'http://factotum.epa.gov/media/' + file.values[0]
            r = requests.get(url)
            if r.status_code == 200:
                return r
    file = fname_list.loc[fname_list['filename'] == fname, 'file']
    if len(file) == 1:
        url = 'http://factotum.epa.gov/media/' + file.values[0]
        r = requests.get(url)
        if r.status_code == 200:
            return r
    return None


def get_content(r, headers, requestOptions=None):
    """Format downloaded pdf content."""
    f = BytesIO(r.content)
    if requestOptions is None:
        raw = parser.from_buffer(f, headers=headers)
    else:
        raw = parser.from_buffer(f, headers=headers,
                                 requestOptions=requestOptions)
    f.close()
    return raw


def pdf_sort(filename, folder, do_OCR=True, all_OCR=False, zipFile=None,
             fname_list=None):
    """Read and organize the PDFs.

    This function is very important. It reads each file and decides what to do
    with it. After cheching if it needs OCR or if it is an MSDS, the function
    will search for Section 3 in the MSDS.

    Args:
        filename (list): [filename, file for tika].
        folder (str): Folder name of pdf location.
        do_OCR (bool, optional): Whether to do OCR.
        all_OCR (bool, optional): Whether to do OCR on all files.

    Returns:
        list: List of many variables, see below.

    """
    # organize the files by filename
    not_pdf = []  # don't do anything with these
    not_sds = []  # not detected as an SDS
    too_3or4 = []  # examine and fix
    no_3or4 = []  # examine and fix
    needs_ocr = []  # pdfs that need ocr
    failed_files = []  # files that failed to load
    split_pdfs = []  # list of pdfs that had multiple msds (successful only)

    # counters
    step0_fail = 0  # pdfs which were not read successfully
    step1_fail = 0  # where a section was not found
    step1_success = 0  # pdfs with text successfully extracted

    # these are the categories for further processing
    to_sec = {}  # text and pdf where the important parts were parsed
    to_old = {}  # text and pdf where the parsing failed
    to_label = {}  # images of labels to parse

    for fname in [filename]:

        # read and process files
        f = fname[0]
        data = {}
        print('----- '+f+' -----')
        logging.debug('%s: Beginning extraction.', f)
        if folder is None:
            path = fname[1]
        else:
            path = os.path.join(folder, fname[1])

        if os.path.splitext(f)[1] != '.pdf':
            print('Not a PDF')
            not_pdf.append(f)
            failed_files.append(f)
            step0_fail += 1
            logging.warning('%s: Not a PDF.', f)
            continue

        headers = {'X-Tika-PDFextractInlineImages': 'false', }
        downloaded = False
        try:
            proc1 = parser.from_file(
                path if zipFile is None else zipFile.open(path),
                headers=headers)
        except PermissionError:
            downloaded = True
            logging.warning('%s: PermissionError, downloading file.', f)
            url = get_url(f, fname_list)  # its actually a response object
            if url is not None:
                proc1 = get_content(url, headers)
            else:
                failed_files.append(f)
                step0_fail += 1
                logging.error('%s: Could not download, skipping file.', f)
                continue

        if proc1['status'] != 200:
            print('Failed to parse')
            failed_files.append(f)
            step0_fail += 1
            logging.error('%s: Failed to read.', f)
            continue

        if proc1['content'] is None:
            needs_ocr.append(f)
            raw1 = []
            content1 = ''
            if not do_OCR:
                print(f+' needs OCR')
                failed_files.append(f)
                step0_fail += 1
                logging.warning('%s: Needs OCR but OCR is not enabled.', f)
                continue
        else:
            content1 = proc1['content']
            if downloaded:
                content1 = unicodedata.normalize('NFKD', content1)
                content1 = content1.replace(u'\xad', '-')
            raw1 = [i for i in content1.splitlines() if
                    len(i.strip()) > 0]
        # proc = proc1
        raw = raw1
        content = content1

        # perform OCR if necessary
        # hasOCR = False
        if do_OCR and (all_OCR or len(raw1) == 0):
            headers2 = {'X-Tika-PDFextractInlineImages': 'true',
                        'X-Tika-OCRTimeout': '300'}
            requestOptions = {'timeout': 300}
            if not downloaded:
                proc2 = parser.from_file(
                    path if zipFile is None else zipFile.open(path),
                    headers=headers2, requestOptions=requestOptions)
            else:
                proc2 = get_content(url, headers2, requestOptions)

            if proc2['content'] is not None:
                content2 = proc2['content']
                if downloaded:
                    content2 = unicodedata.normalize('NFKD', content2)
                    content2 = content2.replace(u'\xad', '-')
                raw2 = [i for i in content2.splitlines()
                        if len(i.strip()) > 0]
                if len([1 for i in raw2 if i in raw1]) == len(raw2):
                    pass
                else:
                    # hasOCR = True
                    f = f+'_OCR'
                    print('Uses OCR: '+f)
                    logging.debug('%s: Uses OCR.', f)
                    # proc = proc2
                    raw = raw2
                    content = content2
            else:
                print('OCR Failed: '+f)
                print('Make sure tesseract is installed and restart tika')
                logging.error('%s: OCR failed.', f)
                failed_files.append(f)
                step0_fail += 1
                continue

        # determine if MSDS
        if not re.search(sds, content) or \
                not re.search(sds2, content):
            # print('Not an SDS: '+f)
            not_sds.append(f)
            step1_success += 1
            logging.debug('%s: Not an MSDS.', f)
            data['raw'] = content
            to_label[f] = data
            continue

    # search for Section 3
        data['raw'] = raw
        ind3 = []
        ind4 = []
        sec3 = []
        sec4 = []
        indCAS = []
        secCAS = []
        for n, val in enumerate(raw):
            if n < len(raw)-1:
                if val.strip()[-1] in ['—', '–', '-', '°']:
                    val = val+raw[n+1].strip()
            if re.search(s3, ' '+val):
                ind3.append(n)
                sec3.append(val)
            if re.search(s4, ' '+val):
                ind4.append(n)
                sec4.append(val)
            se = re.findall(cas1, ' '+val)
            for g in se:
                t = [int(i) for i in (g[0]+g[1])[::-1]]
                if int(g[2]) == np.dot(t, list(range(1, len(t)+1))) % 10:
                    indCAS.append(n)
                    secCAS.append(str(int(g[0])) + '-' +
                                  ('0' + str(int(g[1])))[-2:] +
                                  '-' + str(int(g[2])))
            se2 = re.findall(cas12, ' '+val)
            for g in se2:
                t = [int(i) for i in (g[0]+g[1])[::-1]]
                if int(g[2]) == np.dot(t, list(range(1, len(t)+1))) % 10:
                    indCAS.append(n)
                    secCAS.append(str(int(g[0])) + '-' +
                                  ('0'+str(int(g[1])))[-2:] +
                                  '-' + str(int(g[2])))
                    print('Check: ' + str(int(g[0])) + '-' +
                          ('0' + str(int(g[1])))[-2:] + '-' + str(int(g[2])))

        # special case that needs correcting
        if len(ind3) == 2 and len(ind4) == 1:
            if (re.search(s3_2, ' ' + raw[ind3[0]]) and re.search(
                    s3_3, ' ' + raw[ind3[1]])) and ind3[-1] < ind4[0]:
                s1 = ' '.join(raw[ind3[0]:ind3[1]])
                s2 = ' '.join(raw[ind3[1]:ind4[0]])
                if 'CAS' in s1:
                    if 'CAS' not in s2:
                        ind4[0] = ind3[1]
                    ind3 = [ind3[0]]
                else:
                    if 'CAS' in s2:
                        ind3 = [ind3[1]]
                    else:
                        ind3 = [ind3[0]]

        # repeat headers, remove based on order
        ind3new = []
        if len(pd.unique(sec3)) < len(sec3):
            ind3new.append(ind3[0])
            for n in range(1, len(ind3)):
                if n-1 < len(ind4):
                    if ind3[n] > ind4[n-1]:
                        ind3new.append(ind3[n])
        ind4new = []
        if len(pd.unique(sec4)) < len(sec4):
            ind4new.append(ind4[0])
            for n in range(0, len(ind4)-1):
                if n+1 < len(ind3):
                    if ind4[n] < ind3[n+1] and ind4[n+1] > ind3[n+1]:
                        ind4new.append(ind4[n+1])

        if len(ind3new) > 0:
            ind3 = ind3new
        if len(ind4new) > 0:
            ind4 = ind4new

        # these find  documents which still need to be corrected
        c3 = len(ind3)
        c4 = len(ind4)
        if c3 > 1 and c3 != c4:
            logging.debug('%s: Too many section 3 matches.', f)
            print('Too many section 3 matches: '+f)
        if c3 == 0:
            logging.debug('%s: No section 3 matches.', f)
            print('No section 3 matches: '+f)
        if c4 > 1 and c3 != c4:
            logging.debug('%s: Too many section 4 matches', f)
            print('Too many section 4 matches: '+f)
        if c4 == 0:
            logging.debug('%s: No section 4 matches.', f)
            print('No section 4 matches: '+f)

        data['ind3'] = ind3
        data['ind4'] = ind4
        data['indCAS'] = indCAS
        data['secCAS'] = secCAS
        # data['ocr'] = True if hasOCR else False

        if (c3 > 1 or c4 > 1) and c3 != c4:
            too_3or4.append(f)
            to_old[f] = data
            step1_fail += 1
            continue
        if c3 == 0 or c4 == 0:
            no_3or4.append(f)
            to_old[f] = data
            step1_fail += 1
            continue

        # split up files if they have multiple msds
        if c3 == c4:
            # check index
            if len([1 for i in range(len(ind3)-1)
                    if ind3[i+1] > ind4[i]]) != len(ind3)-1:
                print('Mixed up index: '+f)
                logging.debug('%s: Mixed up index.', f)
                to_old[f] = data
                step1_fail += 1
                continue
            filt = [raw[ind3[i]+1:ind4[i]] for i in range(len(ind3))]
            if len(filt) > 1:
                split_pdfs.append(f)
                f += '_split'

        data['filt'] = filt

        to_sec[f] = data
        step1_success += 1

    return [to_sec, to_old, to_label, step0_fail, step1_fail, step1_success,
            not_pdf, not_sds, too_3or4, no_3or4, needs_ocr, failed_files,
            split_pdfs]
