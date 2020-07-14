# -*- coding: utf-8 -*-
"""Run model.

Created on Tue Dec 17 15:13:07 2019

@author: SBURNS
"""

from model_helper import (model_initialize, load_df, model_build, model_run,
                          results_df)
# import pandas as pd
# import numpy as np
import joblib
from sklearn.model_selection import train_test_split


label = 'testing'
model_initialize(add_groups=[37, 47, 30], label=label)

df = load_df(label=label)
df_train, df_test = train_test_split(df, test_size=0.2)

model_build(df_train=df_train, bootstrap=True, num_runs=11, label=label,
            probab=True)

sen_test = df_test['name']

chem_puclist, chem_removed, chem_problist, chem_pucs_all = model_run(
    sen_test, label)

joblib.dump(chem_puclist, 'chem_proba_puclist' + label + '.joblib')
joblib.dump(chem_removed, 'chem_proba_removed' + label + '.joblib')
joblib.dump(chem_problist, 'chem_proba_problist' + label + '.joblib')
joblib.dump(chem_pucs_all, 'chem_proba_all' + label + '.joblib')

results_df(sen_test, chem_puclist, chem_removed, chem_problist, chem_pucs_all,
           proba_limit=True, label=label)
