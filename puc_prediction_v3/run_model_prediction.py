#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:13:44 2021

@author: jwall01
"""
#Workflow to make predictions based on input string, tuple, list, or DataFrame (from csv or otherwise)

#import pandas as pd
#import numpy as np
from puc_model.model_utils import (run_model_prediction, format_prediction_input)

#Set parameters
label = 'envTest'
pucKind = 'all'#'FO'
modelType = 'SGD'
pred_proba = True

dat = None
# #Load Data
# #625535	ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)	-- Act -- Johnson & Johnson
# #651871	AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)	 -- AHAVA -- Dead Sea Laboratories Ltd.
# #String
# dat = 'ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation) Act Johnson & Johnson'
# #String List
# dat = ['ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation) Act Johnson & Johnson', 
#        'AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation) AHAVA Dead Sea Laboratories Ltd.']
# #Tuple
# dat = ('ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)', 'Act', 'Johnson & Johnson')
# #Tuple List
# dat = [('ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)', 'Act', 'Johnson & Johnson'), 
#        ('AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)', 'AHAVA', 'Dead Sea Laboratories Ltd.')]
# #Missing value
# dat = [('ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)', None, 'Johnson & Johnson'), 
#        ('AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)', 'AHAVA', np.nan)]
# #Dictionary
# dat = {'title': ['ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)',
#                  'AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)'],
#        'brand_name': ['Act', 'AHAVA'],
#        'manufacturer': ['Johnson & Johnson', 'Dead Sea Laboratories Ltd.']}
# #DataFrame
# dat = pd.DataFrame(data=[('ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)', 'Act', 'Johnson & Johnson'), 
#                          ('AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)', 'AHAVA', 'Dead Sea Laboratories Ltd.')],
#                    columns = ['title', 'brand_name', 'manufacturer'])

#Ensure input data fits prediction format
df = format_prediction_input(X=dat)
#Make predictions
df = run_model_prediction(label=label, modelType=modelType, 
                          n_model=None, pucKind=pucKind, df=df, pred_proba=pred_proba)