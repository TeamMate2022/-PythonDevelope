import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date

import time, datetime
import json, csv

import pandas as pd


PAGES_INIT_DB =r'C:\Users\Ali\Desktop\PAGES_INIT_DB.csv'


dicts = {}
profile = 'instagram'
KEYS = ['followers' , 'following' , 'posts' , 'content_type' , 'likes' , 'views' , 'link' , 'last_post_date' , 'last_post_time' , 'save_date' , 'save_time']
dic1 = {'followers': 1111, 'following': 2222}

df = pd.read_csv(PAGES_INIT_DB , index_col = 'username' )
df2 = df.at[profile , 'followers'] , df.at[profile , 'following'] , df.at[profile , 'posts'] , df.at[profile , 'content_type'] , df.at[profile , 'likes'] , df.at[profile , 'views'], df.at[profile , 'link'], df.at[profile , 'last_post_date'], df.at[profile , 'last_post_time'], df.at[profile , 'save_date'], df.at[profile , 'save_time']

for i,j in zip(KEYS,df2):
         
    dicts[i]=j

df3 = df.replace({dicts['followers'] : dic1['followers'] , dicts['following'] : dic1['following']})
print(df3)
# print(df3)
df3.to_csv(PAGES_INIT_DB)