
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
import time, datetime
import json, csv
import pandas as pd


def replace(profile , pages_init_db)
    dicts = {}
    replace_dic = {}
    actual_username, followers, following, posts, last_post_date, last_post_time, likes, views, link, date_save, time_save, content_type = get_profile_information(profile)
    
    replace_dic.update(actual_username)
    replace_dic.update(followers)
    replace_dic.update(following)
    replace_dic.update(posts)
    replace_dic.update(content_type)
    replace_dic.update(likes)
    replace_dic.update(views)
    replace_dic.update(link)
    replace_dic.update(last_post_date)
    replace_dic.update(last_post_time)
    replace_dic.update(date_save)
    replace_dic.update(time_save)
    
    
    df2 = dtfr.at[profile , 'followers'] , dtfr.at[profile , 'following'] , dtfr.at[profile , 'posts'] , dtfr.at[profile , 'content_type'] , dtfr.at[profile , 'likes'] , dtfr.at[profile , 'views'], dtfr.at[profile , 'link'], dtfr.at[profile , 'last_post_date'], dtfr.at[profile , 'last_post_time'], dtfr.at[profile , 'save_date'], dtfr.at[profile , 'save_time']
    for i,j in zip(KEYS,df2):
        dicts[i]=j

    df3 = dtfr.replace({dicts['followers'] : replace_dic[KEY_FOLLOWERS] , dicts['following'] : replace_dic[KEY_FOLLOWING] , dicts['posts'] : replace_dic[KEY_POSTS] , dicts['content_type'] : replace_dic[KEY_CONTENT] , dicts['likes'] : replace_dic[KEY_LIKES] , dicts['views'] : replace_dic[KEY_VIEWS] , dicts['link'] : replace_dic[KEY_LINK] , dicts['last_post_date'] : replace_dic[KEY_LAST_POST_DATE] , dicts['last_post_time'] : replace_dic[KEY_LAST_POST_TIME] , dicts['save_date'] : replace_dic[KEY_SAVE_DATE] , dicts['save_time'] : replace_dic[KEY_SAVE_TIME]})
    
    df3.to_csv(PAGES_INIT_DB)

