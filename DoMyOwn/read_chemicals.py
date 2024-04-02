# -*- coding: utf-8 -*-
"""Create a list of chemicals from different sources.

Created on Thu Apr 16 16:00:55 2020

@author: SBURNS
"""

import re
import numpy as np
import pandas as pd
import os.path
from os import mkdir

import shutil
import urllib.request as request
from contextlib import closing
from urllib.error import URLError

import socket
import json

import zipfile
# need pymysql and xlrd
from urllib.parse import quote  

try:
    from sqlalchemy import create_engine
except ImportError:
    print('SQLAlchemy is necessary if reading from databases')

# try:
from rdkit.Chem import PandasTools
# except ImportError:
    # print('RDKit is necessary if reading from SDF files')


def read_dss(engine):
    """Read info from factotum."""
    print('Reading dsstox true chems from database...')
    sql = 'SELECT DISTINCT true_chemname FROM dashboard_dsstoxlookup;'
    df = pd.read_sql(sql, engine).dropna()
    print('Done')
    print('Chemicals found in dsstoxlookup: ' + str(len(df)))
    return df.rename(columns={'true_chemname': 'chemname'})


def read_rawchems(engine):
    """Read raw chems from factotum."""
    print('Reading rawchems from database...')
    sql = 'SELECT DISTINCT raw_chem_name from dashboard_rawchem;'
    df = pd.read_sql(sql, engine).dropna()
    print('Done')
    print('Chemicals found in rawchem: ' + str(len(df)))
    return df.rename(columns={'raw_chem_name': 'chemname'})


def read_comptox_list(path=''):
    """Read csv of names from comptox."""
    print('Reading comptox csv...')
    #url = 'ftp://newftp.epa.gov/COMPTOX/Sustainable_Chemistry_' + \
    #    'Data/Chemistry_Dashboard/2019/April/DSSTox_Identifiers_' + \
    #    'and_CASRN.xlsx'
    #fname = os.path.basename(url)
    #file_exists = check_file(fname, url, download=True, path=path)
    #if not file_exists:
    #    print('Could not read comptox list')
    #    return None
    df_names = pd.read_excel(r"C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\Scripts\DSSTox_Identifiers_and_CASRN_2021r1.xlsx")
    print('Formatting...')
    df = df_names[['casrn', 'preferred_name']].copy()
    # df['casrn'].nunique() == len(df)
    df = df.set_index('casrn').dropna().copy()
    df['sort'] = df['preferred_name'].apply(lambda x: len(str(x)))
    df1 = df.sort_values(by='sort')[['preferred_name']].copy()
    df1 = df1.rename(columns={'preferred_name': 'chemname'})
    print('Done')
    print('Chemicals found in comptox list: ' + str(len(df1)))
    return df1


def read_synonyms_file(sdfFile, fix_names=False, path=''):
    """Read comptox synonyms file."""
    print('Reading synonyms file...')
    frame = PandasTools.LoadSDF(os.path.join(path, sdfFile),
                                molColName=None,
                                removeHs=False,
                                strictParsing=False)
    # frame = pd.read_csv('names.csv', low_memory=False)
    frame = frame[['Preferred_Name', 'Synonyms']]

    namecol = frame[['Preferred_Name']].copy() \
        .rename(columns={'Preferred_Name': 'chemname'}).dropna()
    syncol = frame[['Synonyms']].copy() \
        .rename(columns={'Synonyms': 'chemname'}).dropna()
    del frame
    print('Formatting...')
    synsplit = syncol['chemname'].str.split('\n', expand=True)
    if fix_names:
        quarter = int(round(len(synsplit)/4))
        synsplit1 = synsplit[:quarter].apply(fix_row, axis=1)
        synsplit2 = synsplit[quarter:quarter*2].apply(fix_row, axis=1)
        synsplit3 = synsplit[quarter*2:quarter*3].apply(fix_row, axis=1)
        synsplit4 = synsplit[quarter*3:].apply(fix_row, axis=1)
        synsplit = pd.concat((synsplit1, synsplit2, synsplit3, synsplit4), axis=0)
        # synsplit = synsplit.apply(fix_row, axis=1)
    comb = pd.concat([synsplit[i].dropna() for i in synsplit.columns]) \
        .dropna().drop_duplicates()
    df = pd.DataFrame(comb, columns=['chemname'])
    df2 = pd.concat([namecol, df]).drop_duplicates()
    print('Done')
    print('Chemicals found in synonyms file: ' + str(len(df2)))
    return df2


def fix_row(x):
    """Fix weird cutoff chemicals."""
    newx = x.copy()
    count = 0
    # print(x.name)
    for i in range(1, len(x)):
        # print(i)
        old = x[i-1] if pd.notna(x[i-1]) else ''
        thisval = x[i]
        nextval = x[i+1] if i < len(x)-1 else ''
        if pd.isna(thisval) and pd.isna(nextval):
            break
        if pd.isna(thisval) and pd.notna(nextval):
            continue
        nextval = nextval if pd.notna(nextval) else ''

        # check if one before and one after are capitolized
        if not re.search(r'^[\dA-Z\(]', old) or \
                not re.search(r'^[\dA-Z\(]', nextval):
            # do nothing
            continue

        # check if needs fix
        bad_vals = ['cis', 'dl', 'sec', 'p', 'o', 'd', 'di', 'sym', 'neo',
                    'exo', 'l', 'gem', 'psi', 'trans', 'sn', 's', 'beta',
                    'all', 'pi']
        bad_ends = ['one', 'ol']
        needs_fix = False
        s1 = re.split(r'[\s\-]', old)[-1]
        if re.search(r'^[\-\s]?[a-z]', thisval) or re.search(r'[\s]$', old):
            needs_fix = True
        if old.endswith('-'):
            needs_fix = False
            continue
        if re.search(r"^(?:[a-z\u03b1-\u03c8\u0391-\u03a9][\']?|[dl]{2})" +
                     r"(?:[\,]\s?[a-z\u03b1-\u03c8\u0391-\u03a9][\']?)*" +
                     r"[\-][\[\(]*[A-Z\d]",
                     thisval):
            needs_fix = False
            continue
        if len(re.split(r'[\s\-]', thisval)[0]) > 3 \
                and len(s1) > 3:
            needs_fix = False
            continue
        if re.split(r'[\-]', thisval)[0].lower() in bad_vals and \
                re.search(r'^[a-zA-Z]{1,3}' +
                          r'[\-][\[\(]*[\u03b1-\u03c8\u0391-\u03a9\dA-Za-z]',
                          thisval):
            needs_fix = False
            continue
        if re.search(r'[\dA-Z]{2,}', s1) or re.search(r'[^a-zA-Z]{3,}', s1):
            needs_fix = False
            continue
        if re.search(r'[^\w\s\-]$', s1):
            needs_fix = False
            continue
        if ((thisval.isupper() and not old.isupper()) and
                len(thisval) > 3) or \
                ((not thisval.isupper() and old.isupper()) and
                 len(old) > 3):
            needs_fix = False
            continue
        if thisval[:3].lower() == old[:3].lower():
            needs_fix = False
            continue
        if re.search(r'^\d+$', re.split(r'[\s]', old)[-1]):
            needs_fix = False
            continue
        if re.split(r'[\-]', old)[-1].lower() in bad_ends:
            needs_fix = False
            continue
        if ((thisval.istitle() and not old.istitle()) and
                len(thisval.split()) > 1) or \
                ((not thisval.istitle() and old.istitle()) and
                 len(old.split()) > 1):
            needs_fix = False
            continue
        # fix
        if needs_fix:
            print(str(i) + ': ' + old + '/' + thisval)
            newx[i-1] = old + thisval
            newx[i] = np.nan
            count += 1

    # if count > 0:
    #     # print('Number changed: ' + str(count))
    return newx


def check_file(fname, url, download=False, path=''):
    """Check to see if the comptox list exists, if not, download it."""
    print('Looking for ' + fname)
    urlname = os.path.basename(url)
    urlpath = os.path.join(path, urlname)
    fpath = os.path.join(path, fname)
    if (not os.path.isfile(fpath) and
            not os.path.isfile(urlpath)) and download:
        print(fname + ' not found, downloading...')
        # from here:https://stackoverflow.com/questions/24023217/
        try:
            with closing(request.urlopen(url)) as r:
                with open(urlpath, 'wb') as f:
                    shutil.copyfileobj(r, f)
        except URLError:
            print('Could not download file: ' + urlname)

    if not os.path.isfile(fpath) and (os.path.isfile(urlpath) and
                                      os.path.splitext(urlname)[-1] == '.zip'):
        print('Unzipping ' + urlname)
        zf = zipfile.ZipFile(urlpath)
        zf.extract(fname, path=path)
        zf.close()
        print('Successfully unzipped')

    if os.path.isfile(fpath):
        print('Found ' + fname)
        return True
    else:
        print('Could not find ' + fname + ', skipping')
        return False


def read_synonyms(fix_names=False, path=''):
    """Read synonyms file."""
    sdfFile = r"C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\Scripts\DSSTox_Synonyms_20161018.sdf"
    #url = 'ftp://newftp.epa.gov/COMPTOX/Sustainable_Chemistry_Data/' + \
        #'Chemistry_Dashboard/DSSTox_Synonyms_20161018.zip'
    #file_exists = check_file(sdfFile, url, download=True, path=path)
    #if not file_exists:
    #    return None
    df = read_synonyms_file(sdfFile, fix_names, path=path)
    return df


def read_databases(raw_chems=False, true_chemname=False):
    """Read database sources."""
    dflist = []
    with open(r"C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\Scripts\mysql.json", 'r') as f:
        cfg = json.load(f)['mysql']

    # check if db is up (https://stackoverflow.com/questions/17434079)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    true_chems = []
    try:
        s.connect((cfg['server'], int(cfg['port'])))
    except socket.gaierror:
        print('connection to database failed')
        df = pd.DataFrame()
    else:
        conn = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                              f'{cfg["password"]}@{cfg["server"]}:' +
                              f'{cfg["port"]}/{cfg["database"]}?charset=utf8',
                              echo=False).connect()

        #conn = create_engine('mysql+pymysql://mmetcalf:' + password + '@mysql-ip-m.epa.gov:3306/prod_factotum', echo=False).connect()
        if raw_chems:
            df = read_rawchems(conn)
            dflist.append(df)
        if true_chemname:
            true_chems = read_dss(conn)
            dflist.append(true_chems)
        conn.close()
    finally:
        s.close()

    if len(dflist) > 0:
        comb = pd.concat(dflist).dropna().drop_duplicates()
        if len(comb) == 0:
            return None
        return comb
    else:
        return None


def read_chemicals(raw_chems=False, true_chemname=False, comptox_list=False,
                   synonyms=False, fix_syn=False, reset=False, save=True,
                   save_folder='', data_folder=''):
    """Produce a list of chemical names.

    This function pulls data from factotum and from various places to create a
    list of unique chemical names. It also deals with saving outputs.

    Args:
        raw_chems (bool): Use chemicals from rawchems table in extractedtext.
        true_chemname (bool): Use chemicals from dsstoxlookup table.
        comptox_list (bool): Use chemicals comptox chemical list.
        synonyms (bool): Use chemicals from comptox synonym list.
        fix_syn (bool): Fix some broken lines in synonym table (may mess up)
        reset (bool): Reread the chemicals from source (don't read saved files)
        save (bool): Save the tables after they're read.
        save_folder (str): Path for saved data. Should be a folder.
        data_folder (str): Path to folder for data and cached lists.

    Returns:
        tcomb (list): A list containing unique chemical names.

    """
    print('Getting chem list...')

    if data_folder != '':
        if not os.path.exists(data_folder):
            mkdir(data_folder)
        elif not os.path.isdir(data_folder):
            print('data_folder needs to be a directory')
            return None

    if save_folder != '':
        if not os.path.exists(save_folder):
            mkdir(save_folder)
        elif not os.path.isdir(save_folder):
            print('save_folder needs to be a directory')
            return None

    fname = 'chemlist_'
    if raw_chems:
        fname += 'raw_'
    if true_chemname:
        fname += 'true_'
    if comptox_list:
        fname += 'comptox_'
    if synonyms:
        fname += 'synonyms_'
        if fix_syn:
            fname += 'fixed_'
    fname = fname.strip('_') + '.csv'

    if not reset and os.path.isfile(os.path.join(save_folder, fname)):
        print('Reading saved list...')
        saved_chems = pd.read_csv(os.path.join(save_folder, fname))
        saved_chems = saved_chems[saved_chems.columns[0]].dropna()
        print('Done')
        return saved_chems

    cas2 = re.compile(r'^(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})[\—\–\-\° ]{1,3}' +
                      r'([\d])$', re.IGNORECASE)
    dflist = []
    # search list from comptox
    if comptox_list:
        comptox_fname = os.path.join(data_folder, 'comptox_list_save.csv')
        if not reset and os.path.isfile(comptox_fname):
            print('Reading saved comptox list...')
            df1 = pd.read_csv(comptox_fname).dropna()
            print('Done')
        else:
            df1 = read_comptox_list(path=data_folder)

        if df1 is not None:
            dflist.append(df1)
            if save:
                df1.to_csv(comptox_fname, index=False)
        else:
            fname = fname.replace('comptox', '')

    # get chemicals from factotum
    db_fname = 'db_save_'
    if raw_chems:
        db_fname += 'raw_'
    if true_chemname:
        db_fname += 'true_'
    db_fname = os.path.join(data_folder, db_fname.strip('_') + '.csv')
    if not reset and os.path.isfile(db_fname):
        print('Reading saved database list...')
        df2 = pd.read_csv(db_fname).dropna()
        print('Done')
    else:
        df2 = read_databases(raw_chems, true_chemname)

    if df2 is not None:
        dflist.append(df2)
        if save:
            df2.to_csv(db_fname, index=False)
    else:
        fname = fname.replace('raw', '')
        fname = fname.replace('true', '')

    # read synonyms file
    if synonyms:
        synonyms_fname = os.path.join(
            data_folder,
            'synonyms_' + ('fixed_' if fix_syn else '') + 'save.csv')
        if not reset and os.path.isfile(synonyms_fname):
            print('Reading saved synonyms list...')
            df3 = pd.read_csv(synonyms_fname).dropna()
            print('Done')
        else:
            df3 = read_synonyms(fix_names=fix_syn, path=data_folder)

        if df3 is not None:
            dflist.append(df3)
            if save:
                df3.to_csv(synonyms_fname, index=False)
        else:
            fname = fname.replace('synonyms', '')

    # format and compile the list of chemicals
    print('Combining lists...')
    if len(dflist) == 0:
        print('No chemicals found')
        return None
    cq = pd.concat(dflist).apply(lambda x: x.str.lower().str.strip())
    df = cq['chemname'].dropna().drop_duplicates()
    df_u = pd.unique(df.str.strip().str.lower())
    tcomb = pd.Series([i for i in df_u if not re.search(cas2, i)])

    # saving chemicals
    if save and len(tcomb) > 0:
        fname = re.sub(r'[\_]+', '_',
                       os.path.splitext(fname)[0]).strip('_') + '.csv'
        tcomb.to_csv(os.path.join(save_folder, fname), index=False)

    print('Done')
    return tcomb


if __name__ == '__main__':
    df = read_chemicals(raw_chems=False,
                        true_chemname=True,
                        comptox_list=True,
                        synonyms=True, fix_syn=True,
                        reset=False,
                        save=True,
                        save_folder='chems',
                        data_folder='chems_data')
    df = read_chemicals(raw_chems=True,
                        true_chemname=False,
                        comptox_list=True,
                        synonyms=True, fix_syn=True,
                        reset=False,
                        save=True,
                        save_folder='chems',
                        data_folder='chems_data')
    df = read_chemicals(raw_chems=True,
                        true_chemname=True,
                        comptox_list=True,
                        synonyms=True, fix_syn=True,
                        reset=False,
                        save=True,
                        save_folder='chems',
                        data_folder='chems_data')
