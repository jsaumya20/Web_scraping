# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 18:11:10 2022

@author: jsaum
"""

from google_play_scraper import app
import pandas as pd
import numpy as np
from google_play_scraper import Sort, reviews_all

app_ids =pd.read_excel("google_play_store_app_ids.xlsx")

for row in app_ids.itertuples():
    name = row.App_Name
    app_id = row.App_id
    
    try:
        us_reviews = reviews_all(app_id,
        sleep_milliseconds=0, # defaults to 0
        lang='en', # defaults to 'en'
        country='us', # defaults to 'us'
        sort=Sort.NEWEST ) # defaults to Sort.MOST_RELEVANT
        
                
    except Exception as e:
        print("Exception while getting reviews for: %s : %s"%(name, repr(e)))
    
    try:
        df_temp = pd.DataFrame(np.array(us_reviews),columns=['review'])
        df_temp = df_temp.join(pd.DataFrame(df_temp.pop('review').tolist()))
        
        file_name = name + "google_play_store" + ".csv"
        df_temp.to_csv( file_name,encoding = 'utf-8',index= False)
    
    except Exception as e:
        print("Exception while converting df to csv for: %s : %s"%(name, repr(e)))
    
    print(name,": App data successfully Scraped!")

    

    