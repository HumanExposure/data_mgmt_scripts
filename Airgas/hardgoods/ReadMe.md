This script is the generic extraction script ([https://github.com/HumanExposure/data_mgmt_scripts/tree/master/generic_script/scripts](https://github.com/HumanExposure/data_mgmt_scripts/tree/master/generic_script)), with a few edits 

Changes made:

Handled the comptox synonym file in 4 pieces, then recombined them to avoid memory error (lines 99-107 in read_chemicals.py)

Changed line 202 in transform.py to xnew['name'] = x['name'] + ' (CI ' + str(x['ci_color']) + ')'

Changed 'from pymysql import escape_string' in formatting .py to:

import pymysql

from pymysql.converters import escape_string

Changed paths in run_extraction.py

Changed paths and filenames in transform.py
