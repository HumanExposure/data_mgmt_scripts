# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:20:16 2020

@author: ALarger

This script reads in a CSV of product data and folder of corresponding product images, and creates products through the Factotum API
To run, you must have a Factotum login
Make sure all product images have been resized to 180x180 before running
"""

import json
import requests
import base64
import pandas as pd
import logging
import os


#Edit this section to reflect the folders and file names being used for this group
picFolder = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Big D/Big D New' #Folder pictures are in
folder = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Big D/Big D New' #Folder the csv with product info is in
file = 'big d webpage create products.csv' #Name of file with product data


os.chdir(folder)
logging.basicConfig(filename='logfile.log',level=logging.INFO)
server_url = "https://ccte-api-factotum.epa.gov/"


#Get auth token
username = input("Enter username: ")
password = input("Enter password: ")
post_data = '{ "data": { "type": "token","attributes": { "username": "'+username+'","password": "'+password+'"}}}'
response = requests.post(server_url+'token/', headers={'Content-Type': 'application/vnd.api+json'},data=post_data)
token = "Bearer "+json.loads(response.text)['token']


#This reads the column headers from the product csv, creates a json for each row, and sends the json to the Factotum API. 
#If you use different column headers than what's on the product csv template in Factotum, then change the name in the brackets after df.loc[n] to reflect the column name. 
#If the csv doesn't have a particular field, comment that line out
df = pd.read_csv(file, dtype=str).fillna('')
for n in range(0,len(df)): 
    ddid = df.loc[n]['data_document_id']
    attributes = {}
    attributes["brand"] = df.loc[n]["brand_name"]    
    attributes["color"] = df.loc[n]["color"]
    attributes["epa_reg_number"] = df.loc[n]["epa_reg_number"]
    attributes["large_image"] = df.loc[n]["large_image"]
    attributes["long_description"] = df.loc[n]["long_description"]
    attributes["manufacturer"] = df.loc[n]["manufacturer"]
    attributes["medium_image"] = df.loc[n]["medium_image"]
    attributes["model_number"] = df.loc[n]["model_number"]
    attributes["name"] = df.loc[n]["title"]
    attributes["product_url"] = df.loc[n]["url"]
    attributes["short_description"] = df.loc[n]["short_description"]
    attributes["size"] = df.loc[n]["size"]
    attributes["thumb_image"] = df.loc[n]["thumb_image"]
    attributes["upc"] = df.loc[n]["upc"]
    
    if df.loc[n]["image_name"] != '':
        image = open((picFolder+'/'+df.loc[n]["image_name"]),'rb')
        image_read = image.read()
        image_64_encode = base64.b64encode(image_read).decode('utf-8')
        attributes["image"] = image_64_encode
    
    data = {  
      "data": {    
          "attributes": attributes,
          "relationships": {
              "dataDocuments": {
                  "data": [
                      {
                          "id": str(ddid),
                          "type": "dataDocument"
                      }
                  ]
              }
          },
          "type": "product"
      }
    }
    
    payload = json.dumps(data)
    # print(payload)
    
    response = requests.post(server_url+'products/', payload, headers={"Authorization": token, "content-type" : "application/vnd.api+json"})
    logging.info(json.loads(response.text))

    if response.status_code != 201: 
        print('error!',ddid,response.status_code)
        if response.status_code == 401: #Auth token expired. Get a new one and try again
            post_data = '{ "data": { "type": "token","attributes": { "username": "'+username+'","password": "'+password+'"}}}'
            response = requests.post(server_url+'token/', headers={'Content-Type': 'application/vnd.api+json'},data=post_data)
            token = "Bearer "+json.loads(response.text)['token']
            
            response = requests.post(server_url+'products/', payload, headers={"Authorization": token, "content-type" : "application/vnd.api+json"})
            logging.info(json.loads(response.text))
