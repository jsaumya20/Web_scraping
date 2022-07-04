# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 15:44:39 2022

@author: jsaum
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 17:51:20 2022

@author: jsaum
"""

from bs4 import BeautifulSoup
import requests, lxml, re, json
from datetime import datetime
import pandas as pd
import numpy as np
from google_play_scraper import app ,Sort, reviews_all
import matplotlib.pyplot as plt

books_app_data = pd.read_csv("Books_app_details.csv",index_col=False)
books_app_data['App Id']

temp=[]
import os
counter =0
failed_apps = []
for appId in books_app_data['App Id']:
    try:
        app_data = app(
        appId,
        lang='en', # defaults to 'en'
        country='us' # defaults to 'us
        )
    except Exception as e:
        print("Error while getting info about %s: Reason: %s"%(appId, repr(e)))
        failed_app = {"appId":appId, "reason": repr(e) }
        failed_apps.append(failed_app)
        continue
    temp.append(app_data)
    if len(temp) == 100:
        counter +=1
        temp_df = pd.json_normalize(temp)
        if not os.path.isfile('Books_scraped_app_data.csv'):
            temp_df.to_csv('Books_scraped_app_data.csv',encoding = 'utf-8',index= False)
        else:
            temp_df.to_csv('Books_scraped_app_data.csv',mode= 'a', encoding = 'utf-8',index= False, header=False)
        temp = []
    print("Done with batches : %d" %(counter))

if not os.path.isfile('Books_failed_apps.csv'):
    failed_app_df = pd.json_normalize(failed_apps)
    failed_app_df.to_csv('Books_failed_apps.csv',encoding = 'utf-8',index= False)
        
print("Done!! :)")
