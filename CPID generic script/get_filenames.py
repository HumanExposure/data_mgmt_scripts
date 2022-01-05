# -*- coding: utf-8 -*-
"""Make list of files for each datagroup.

Created on Wed Apr 22 11:45:05 2020

@author: SBURNS
"""

import pandas as pd
import os.path
from os import mkdir
import json
import socket
from pymysql import escape_string
from sqlalchemy import create_engine


def read_df(group, engine):
    """Read info from factotum."""
    sql = 'SELECT file, data_group_id FROM dashboard_datadocument WHERE ' + \
          f'data_group_id = {group};'
    df = pd.read_sql(escape_string(sql), engine)
    return df.dropna()


def read_data(groups):
    """Make SQL connectable."""
    with open('mysql.json', 'r') as f:
        cfg = json.load(f)['mysql']

    # check if db is up (https://stackoverflow.com/questions/17434079)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((cfg['server'], int(cfg['port'])))
    except socket.gaierror:
        print('connection to database failed')
        return None
    else:
        print('successfully connected to database')
    finally:
        s.close()

    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           convert_unicode=True, echo=False)

    data_list = {i: read_df(i, engine) for i in groups}

    engine.dispose()
    return data_list


if __name__ == '__main__':
    walmart_groups = [17, 18, 19, 23, 24, 26]
    folder = 'file_list'
    if not os.path.exists(folder):
        mkdir(folder)
    dflist = read_data(walmart_groups)
    for key, val in dflist.items():
        val['file'].to_csv(os.path.join(folder, f'file_list_group_{key}.csv'),
                           index=False)
