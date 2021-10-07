#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 20:31:13 2021

@author: jwall01
"""

'''
Script used to try to batch creation of xdata when the data is too large to do at once.
This script is meant to handle memory allotment error crashes/kills.
'''
import os
import joblib
import torch
import sys
from data_processing import load_doc_embeddings, get_vector

def xdata_components_dump (lab='', compDir='', i=None):
    if not os.path.isfile(f'{compDir}xdata_vector_{i}.joblib'):
        print(f'Prepping file {i}')
        doc_embeddings = load_doc_embeddings()
        doc_embeddings.load_state_dict(
            torch.load(f'{compDir}PUC_doc_embedding{lab}.pt'))
        doc_embeddings.eval()
        x = joblib.load(f'{compDir}xdata{lab}_components.joblib')[i]
        tmp = get_vector(x['name'], doc_embeddings)
        #Dump dictionary of product_id with associated vector        
        joblib.dump({ x.iloc[j].product_id: tmp[j] for j in range(len(tmp))}, 
                    f'{compDir}xdata_vector_{i}.joblib')
        print(f'...File {i} saved...')
        try:
            joblib.load(f'{compDir}xdata_vector_{i}.joblib')
        except EOFError:
            print("...Found EOFError...deleting file just created")
            os.remove(os.path.abspath(f'{compDir}xdata_vector_{i}.joblib'))
        del x, tmp        
    else:
        print(f'File {i} already exists...')   
    
if __name__ == '__main__':
    xdata_components_dump(lab=sys.argv[1], compDir=sys.argv[2], i=int(sys.argv[3]))