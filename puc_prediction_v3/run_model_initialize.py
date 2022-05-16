# -*- coding: utf-8 -*-
"""
Run model initialization to pull data, clean, and prep for vectorization.

Created on Wed Sep 23 2019

@author: JWALL01
"""
from puc_model.model_initialize import (model_initialize)
from puc_model.data_processing import (load_env_file)

env = load_env_file("env.json")

model_initialize(add_groups=env["model_initialize"]["groups"], 
                 label=env["model_label"], 
                 recordMin=env["model_initialize"]["recordMin"],
                  pucType=env["model_initialize"]["pucType"], 
                  overwrite=env["model_initialize"]["overwrite"])

#label = 'factotum_20211129'
# model_initialize(add_groups=[37, 47, 30], label=label, recordMin=100,
#                   pucType='all', overwrite=True)
