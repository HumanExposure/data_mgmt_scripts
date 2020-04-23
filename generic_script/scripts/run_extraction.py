# -*- coding: utf-8 -*-
"""Script for procsssing MSDS and produt labels.

Created on Fri Oct 18 11:34:22 2019

@author: SBURNS
"""

import os
import sys
import pandas as pd
import logging
import time
# from sqlalchemy import create_engine
# import json
# import re
import zipfile
from tika.tika import killServer

from pdf_import import pdf_sort, read_fname_df
from label_search import fun_label_search
from chem_search import (fun_chemicals, fun_chemicals_add, fun_chemicals_old,
                         fun_sec_search, fun_wide_search)
from formatting import chem_format, fix_dict
from read_chemicals import read_chemicals


def pdf_extract(fname, folder, tcomb, do_OCR=True, all_OCR=False,
                zipFile=None, fname_list=None):
    """Take a filename and return chemical info."""
    # read pdf
    f = fname[0]
    comb = pdf_sort(fname, folder, do_OCR, all_OCR, zipFile, fname_list)

    # break out output (this info will be used to log)
    # step0_fail = comb[3]
    # step1_fail = comb[4]
    # step1_success = comb[5]
    # not_pdf = comb[6]
    # not_sds = comb[7]
    # too_3or4 = comb[8]
    # no_3or4 = comb[9]
    needs_ocr = comb[10]
    failed_files = comb[11]
    split_pdfs = comb[12]

    # data for processing
    to_sec = comb[0]  # text and pdf where the important parts were parsed
    to_old = comb[1]  # text and pdf where the parsing failed
    to_label = comb[2]  # images of labels to parse

    # run functions
    sc = []
    named = []
    casno = []
    nlabel = []

    # keys for all these were removed
    # chemicals: key to section to list
    # chemicals_old: key to list
    # chemicals_add: key to list

    # sec_search: key to section to list of dicts
    # sec_search_wide: key to list of dicts
    # old_search: key to list of dicts

    # label_search: key to list
    # label_search2: key to list (not anymore)

    # search for information
    # all of these loops are 1 item long
    for key, val in to_sec.items():
        sc.append('sec')

        chemicals = fun_chemicals(key, val)
        chemicals_add = fun_chemicals_add(key, val, chemicals)
        sec_search = fun_sec_search(key, val, tcomb)
        sec_search_wide = fun_wide_search(key, val, tcomb)

        named = named + [j for i in sec_search for j in i]
        named = named + sec_search_wide
        casno = casno + [j for i in chemicals for j in i]
        casno = casno + chemicals_add

    for key, val in to_old.items():
        sc.append('old')

        chemicals_old = fun_chemicals_old(key, val)
        old_search = fun_wide_search(key, val, tcomb)

        named = named + old_search
        casno = casno + chemicals_old

    for key, val in to_label.items():
        sc.append('label')

        label_search = fun_label_search(key, val, tcomb)

        nlabel = nlabel + label_search

    # aggregate names
    named = [j for i in named for j in fix_dict(i)]
    chemct1 = len(named)
    chemct2 = len(pd.unique(casno)) + len(pd.unique(nlabel))
    logging.debug('%s: %s chems to df_search, %s other.', f, str(chemct1),
                  str(chemct2))
    df_search = pd.DataFrame(chem_format(named))
    df_search.drop_duplicates(inplace=True)

    # aggregate cas
    casno = [i for i in list(pd.unique(casno))
             if ('cas' in df_search.columns and
                 i not in df_search['cas'].values)
             or ('cas' not in df_search.columns)]
    to_add = [{'name': '', 'cas': n, 'min_wt': '', 'cent_wt': '',
                       'max_wt': '', 'ci_color': ''} for n in casno]
    to_add_df = pd.DataFrame(to_add)

    # aggregate label info
    nlabel = chem_format([i for i in list(pd.unique(nlabel))
                          if ('name' in df_search.columns and
                              i not in df_search['name'].values)
                          or ('name' not in df_search.columns)])
    to_add_label = [{'name': n, 'cas': '', 'min_wt': '', 'cent_wt': '',
                     'max_wt': '', 'ci_color': ''} for n in nlabel]
    to_add_label_df = pd.DataFrame(to_add_label)

    # combine
    df_comb = pd.concat([df_search, to_add_df, to_add_label_df]) \
        .reset_index(drop=True)
    if len(df_comb) == 0:
        df_comb = pd.DataFrame({'name': '', 'cas': '', 'min_wt': '',
                                'cent_wt': '', 'max_wt': '', 'ci_color': ''},
                               index=[0])
    df_comb = df_comb.loc[df_comb.apply(lambda x: 0 if x.sum().strip()
                                        == '' else 1, axis=1) == 1]

    if (chemct1 == 0 and chemct2 != 0) and len(df_comb) == 0:
        logging.warning('%s: Check documents for removed chemicals.', f)

    df_comb.insert(0, 'filename', f)
    # df_comb.insert(0, 'filename', f.split('.pdf')[0] + '.csv')
    # df_store.append(df_comb)

    # create file info for log
    dinfo = {}
    dinfo['filename'] = f
    dinfo['OCR'] = True if len([i for i in needs_ocr if f in i]) > 0 else False
    dinfo['split'] = True if len([i for i in split_pdfs if f in i]) > 0 \
        else False
    if f in failed_files:
        dinfo['debug'] = 'failed'
    elif len(sc) == 0:
        dinfo['debug'] = 'missing'
    else:
        dinfo['debug'] = ','.join(list(pd.unique(sc)))
        if len(sc) > 1:
            print(sc)
            logging.warning('%s: Sorted into multiple sections.', f)
    dinfo['num_found'] = len(df_comb)

    logging.debug('%s: OCR=%s, split=%s, section=%s', dinfo['filename'],
                  str(dinfo['OCR']), str(dinfo['split']), dinfo['debug'])
    logging.info('%s: %s chemicals found.', dinfo['filename'],
                 str(dinfo['num_found']))

    # info_df.append(dinfo)

    return df_comb, dinfo


if __name__ == '__main__':
    # change parameters here
    do_OCR = True
    all_OCR = False
    out_folder = os.path.join(os.getcwd(), 'output')
    folder = os.path.join(os.getcwd(), 'pdf')  # default folder

    # check folders
    if not os.path.isdir(out_folder):
        print('Output folder not found, creating folder...')
        if os.path.exists(out_folder):
            print('Output folder name conflict, please change name')
            sys.exit()
        else:
            try:
                os.mkdir(out_folder)
            except OSError:
                print('Could not automatically create directory, exiting')
            else:
                print('Successfully created directory')

    # get label for output files
    label = ''
    if len(sys.argv) > 1:
        label = os.path.split(sys.argv[1])[-1].replace('.', '_') + '_'
    elif len(sys.argv) > 3:
        print('Too many arguments, exiting script')
        sys.exit()

    # parse arguments. arguments override folder
    zipFile = False
    if len(sys.argv) == 1:
        if not os.path.isdir(folder):
            print('PDF folder not found: ' + str(folder))
            sys.exit()
        file_iter = os.listdir(folder)
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if os.path.isdir(arg):
            folder = arg
            file_iter = os.listdir(folder)
        elif os.path.isfile(arg):
            ext = os.path.splitext(arg)[1]
            folder = None
            if ext.lower() == '.zip':
                zipFile = True
                zf = zipfile.ZipFile(arg)
                file_iter = zf.infolist()
            else:
                file_iter = [arg]
        else:
            print('File/folder not found, exiting script')
            sys.exit()
    elif len(sys.argv) == 3:
        arg1 = sys.argv[1]  # path to list
        arg2 = sys.argv[2]  # folder
        if os.path.isdir(arg2):
            folder = arg2
        else:
            print('Second argument must be a folder, exiting script')
            sys.exit()
        if os.path.isfile(arg1) and os.path.splitext(arg1)[-1] == '.csv':
            fname_df = pd.read_csv(arg1).drop_duplicates()
            file_iter = fname_df[fname_df.columns[0]]
            # check files
            bad = False
            for i in file_iter:
                tpath = os.path.join(folder, i)
                if not os.path.isfile(tpath):
                    bad = True
                    print('File ' + i + 'does not exist in ' + folder)
            if bad:
                print('Make sure all files exist. Exiting.')
                sys.exit()
            else:
                print('All files found.')
        else:
            print('First argument must be a csv of files names, exiting')
            sys.exit()

    # start logging
    stime = time.strftime('%Y-%m-%d_%H-%M-%S')
    logging.basicConfig(filename=os.path.join(out_folder, 'extract_' + label
                                              + stime +
                                              '.log'), filemode='w',
                        format='[%(levelname)s] %(asctime)s: %(message)s',
                        level=logging.INFO)

    if do_OCR and not all_OCR:
        logging.info('OCR is enabled for files with no text.')
    elif do_OCR and all_OCR:
        logging.info('OCR is enabled for all files.')
    elif not do_OCR and all_OCR:
        logging.warning('OCR is not enabled.')
    else:
        logging.info('OCR is not enabled.')

    num_found = len([i for i in file_iter if os.path.splitext(
        i.filename if zipFile else i
        )[1] == '.pdf'])
    logging.info('%s PDFs found.', str(num_found))

    if num_found == 0:
        print('No PDFs found, exiting')
        logging.error('No PDFs found, exiting')
        sys.exit()

    # get chemical list
    logging.debug('Getting chem list...')
    tcomb = read_chemicals(raw_chems=False,
                           true_chemname=True,
                           comptox_list=True,
                           synonyms=True, fix_syn=True,
                           reset=False,
                           save=True,
                           save_folder='chems_list',
                           data_folder='chems_data')
    logging.debug('Done. %s chemicals found.', str(len(tcomb)))
    logging.debug('Getting filename list...')
    fname_list = read_fname_df()
    logging.debug('Done')

    # iterate through files
    # tcomb = read_df()
    df_store = []
    info_df = []
    for f in file_iter:
        fname = os.path.split(f.filename)[1] if zipFile else \
            os.path.basename(f)
        zfile = zf if zipFile else None

        try:
            d1, d2 = pdf_extract([fname, f], folder, tcomb, do_OCR, all_OCR,
                                 zfile, fname_list)
        except (KeyboardInterrupt, SystemExit):
            logging.exception('%s: Run stopped', fname)
            raise
        except:
            logging.exception('%s: Unexpected error, continuing run', fname)
        else:
            df_store.append(d1)
            info_df.append(d2)

    if zipFile:
        zf.close()

    killServer()  # may need to kill manually

    if len(df_store) == 0:
        df_store.append(pd.DataFrame())
    df_all = pd.concat(df_store).reset_index(drop=True)
    file_prop = pd.DataFrame(info_df)

    # write info file
    df_all.to_csv(os.path.join(out_folder,
                               'chemical_data_' + label + stime + '.csv'),
                  index_label='row')
    file_prop.to_csv(os.path.join(out_folder,
                                  'file_info_' + label + stime + '.csv'),
                     index=False)
