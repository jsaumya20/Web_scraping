# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 10:34:06 2022

@author: jsaum
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 17:22:00 2022

@author: jsaum
"""
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd

from openpyxl import load_workbook


def get_reviews_for_page(URL,review_title):
    try:
        global reviews_count
        global pages_count
        source = requests.get(URL)
        source.raise_for_status() #method will throw a error if the url is invalid 
        source.ok
        soup = BeautifulSoup(source.text ,'html.parser')
        
        reviews = soup.find('div',class_= 'postlist').find_all("li")
        for review in reviews :
            try:
                reviews_count +=1
                temp = {"review_author":"", "review_message":"",
                        "review_time":"","review_likes_count":"",
                        "review_question":"","URL":""}
                review_author = review.find('a',class_ ='mp-username username')
                if review_author:
                    temp["review_author"] = review_author.text
                review_message = review.find('div' ,class_ ='message')
                if review_message:
                    temp["review_message"] = review_message.text
                review_time = review.find('div' ,class_ ='time')
                if review_time:
                    temp["review_time"] = review_time.text    
                review_likes_div = review.find('div' ,class_ ='social')
                if review_likes_div:
                    review_likes_count = review_likes_div.find('i' ,class_ ='stat')
                    if review_likes_count:
                        temp["review_likes_count"] = review_likes_count.text
                temp["review_question"] = review_title
                temp["URL"] = URL
                
                all_reviews_info.append(temp)
            except Exception as e:
                print("Exception in review %s: %s" % (review.text, repr(e)))
                continue
        pages_count += 1
    except Exception as e:
        print("Exception in get_reviews_for_page: %s"%(repr(e)))
    
def get_reviews_for_searchresult(URL):
    try:
        source = requests.get(URL)
        source.raise_for_status() #method will throw a error if the url is invalid 
        soup = BeautifulSoup(source.text ,'html.parser')
        review_title = soup.find('div' ,class_ ='breadcrumb').find('h1',class_='ptitle').text
    except:
        return
    base_url = URL.split(".html")[0]
    max_pages = 0
    pages = 2
    single_page = True
    try:
        last_page_url = soup.find('span', class_ = 'first_last').find('a')['href']
    except:
        last_page_url = None
        
    if last_page_url is not None:
        tokens = last_page_url.split("-")
        max_pages = int(tokens[-1].split(".")[0])
        single_page = False
    if(single_page):
        get_reviews_for_page(base_url + ".html",review_title)
    else:
        get_reviews_for_page(base_url + ".html",review_title)
        while pages <= max_pages:
            get_reviews_for_page(base_url+ "-" + str(pages) + ".html",review_title)
            pages += 1
            
book = load_workbook('Android_central_URL.xlsx')
sheets = [ws.title for ws in book.worksheets]
pages_count = 0
reviews_count = 0
done_sheets = ["Instagram","Youtube","Clash of Clans","TikTok","PUBG","Garena Free Fire","whatsapp"]
for sheet_name in sheets:
    if sheet_name in done_sheets:
        print("Skipping %s since its already done."%(sheet_name))
        continue
    print("Processing urls in sheet:", sheet_name)
    df = pd.read_excel("Android_central_URL.xlsx",sheet_name=sheet_name,header= None,index_col=0)
    df.index.names = ['List']
    all_reviews_info = []
    
    
    for i in range(len(df)):
        get_reviews_for_searchresult(df.index[i])
            
    all_reviews_info_df = pd.json_normalize(all_reviews_info)
    try:
        file_path = "Android_central_Comments_" + sheet_name.replace(" ", "-") + ".xlsx"
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
            all_reviews_info_df.to_excel(writer, sheet_name = sheet_name, index_label=None, header=True, encoding = 'utf-8', index= False)
        
            
        #all_reviews_text = json.dumps(all_reviews_info, indent=4)
    except Exception as e:
        print("Exception while writing for sheet: %s : %s"%(sheet_name, repr(e)))


#print(all_reviews_text)
print(f"Total pages scraped: {pages_count}")
print(f"Total comments scraped: {reviews_count}")