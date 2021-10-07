# -*- coding: utf-8 -*-
"""
Run model initialization to pull data, clean, and prep for vectorization.

Created on Wed Sep 23 2019

@author: JWALL01
"""
from puc_model.model_initialize import (model_initialize)

label = 'envTest'

model_initialize(add_groups=[37, 47, 30], label=label, recordMin=100,
                 pucType='all', overwrite=True)
