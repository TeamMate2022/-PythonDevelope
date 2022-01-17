# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 18:38:26 2021

@author : Amirhosein syh
"""


from typing import Counter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
import math
import time
import datetime
import json
import csv
import os
import pandas as pd

# config:
DRIVER_PATH = os.path.dirname(__file__) + r"/chromedriver"
driver = webdriver.Chrome(DRIVER_PATH)

INSTAGRAM = 'https://www.instagram.com/'
# USERNAME = 'annonymous_test'
# PASSWORD = 'this is a test 123'

USERNAME = "tes_tthis"
PASSWORD = "this is a test 123"

DEBUG = True
COOKIES = False
INIT_DATABASE_STATUS = False

APP_FOLDER = r'/instascraper data'

CSV_FILE = os.path.dirname(__file__) + APP_FOLDER
PROFILES_USERNAME_DB = os.path.dirname(__file__) + r"/user_profiles_db.txt"
PAGES_INIT_DB = os.path.dirname(__file__)+ APP_FOLDER + r"/pages_init_db.csv"
WATCHLIST_DB = os.path.dirname(__file__) + APP_FOLDER+ r"/watchlist_db.txt"
USER_INFORMATIONS = os.path.dirname(__file__) + APP_FOLDER + r"/user_basic_informations.txt"
RESULT_PATH = os.path.dirname(__file__) + APP_FOLDER + r"/result.txt"
TASKMANAGER_PATH = os.path.dirname(__file__) + APP_FOLDER + r"/task_manager.csv"

LOADING_PERIOD = 16
PAGE_INTERACT_PERIOD = 6
MAX_POSTS = 5

WATCHLIST_PERIOD = 30
WATCHLIST_REFRESH = 30

# TODO :
#  1. check that user_profiles.txt exist, otherwise run script to get profiles (def retrive_usernames)
#  2. check that result.txt file exist, otherwise create a new file

# keys:
KEY_USERNAME = "username"
KEY_POSTS = "posts"
KEY_FOLLOWERS = "followers"
KEY_FOLLOWING = "following"
KEY_ANALYSED_POSTS = "analysed_posts"
KEY_LAST_POST_DATE = "last_post_date"
KEY_LAST_POST_TIME = "last_post_time"
KEY_LIKES = "likes"
KEY_VIEWS = "views"
KEY_ENGAGEMENT = "engagement"
KEY_LINK = 'link'
KEY_SAVE_TIME = 'save_time'
KEY_SAVE_DATE = 'save_date'
KEY_CONTENT = 'content_type'
KEY_REMAIN_TIME = 'remain_time'

CLEANED_FILE = False
FIRST_TIME_CSV = True

APPEND = 'a'
WRITE = 'w'

def create_folder(folder_name):
    os.makedirs(os.getcwd() + folder_name)

def login():
    driver.get(INSTAGRAM)
    # accept cookies:
    if COOKIES:
        time.sleep(PAGE_INTERACT_PERIOD)
        driver.find_element_by_xpath("//button[contains(text(), 'Accept All')]").click()
    # login
    time.sleep(LOADING_PERIOD)
    username = driver.find_element_by_css_selector("input[name='username']")
    password = driver.find_element_by_css_selector("input[name='password']")
    username.clear()
    password.clear()
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    driver.find_element_by_css_selector("button[type='submit']").click()
    time.sleep(PAGE_INTERACT_PERIOD)

def init_instagram():
    """ we will login to instagram and make our bot ready """
    login()
    # save login info?
    time.sleep(PAGE_INTERACT_PERIOD)
    driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
    # turn off notif
    time.sleep(PAGE_INTERACT_PERIOD)
    driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

def get_usernames(PROFILES_USERNAME_DB):
    """ this method will read usernames from user_profiles file"""
    return open(PROFILES_USERNAME_DB, 'r').read().split('\n')

def find_profile(username):
    print(f'start to search for {username}')
    # searchbox
    time.sleep(LOADING_PERIOD)
    searchbox = driver.find_element_by_css_selector("input[placeholder='Search']")
    searchbox.clear()
    searchbox.send_keys(username)
    time.sleep(PAGE_INTERACT_PERIOD)
    searchbox.send_keys(Keys.ENTER)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(PAGE_INTERACT_PERIOD)

def go_to_profile(username):
    print("try to open page by it's URL")
    driver.get(INSTAGRAM + username)

def get_last_post_link():
    print('want to get last post link')
    post_url = ""
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        attr = link.get_attribute('href')
        if '/p/' in attr:
            post_url = attr
            break
    print(f'last post url {post_url}')
    return post_url

def get_post_information(link):
    """ with this method we can collect post information by it's link"""
    print(f'try to open {link} and collect data')
    driver.get(link)
    time.sleep(PAGE_INTERACT_PERIOD)

    try:
        likes = (((driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/a/span").text).replace(',', '')))
        view = 0
    except:
        driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span").click()
        time.sleep(PAGE_INTERACT_PERIOD)
        likes = (((driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div[4]/span").text).replace(',', '')))
        view = (((driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span/span").text).replace(',', '')))

    
    post_datetime = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[2]/a/time").get_attribute('datetime')
    post_date, post_time = post_datetime.split("T")
    post_time = post_time[:len(post_time)-5]
    saving_date, saving_time = get_current_time_and_date()

    if int(view) > 0:
        content_type = 'video'
    else:
        content_type = 'image'

    print('---------------------------------------------------------------')
    print(likes, view, content_type, post_date, post_time, link, saving_date, saving_time)

    return (int(likes), int(view), content_type, post_date, post_time, link, saving_date, saving_time)


def get_profile_information(username):
    print(f'start to collect data from {username} user')
    # find_profile(username)
    go_to_profile(username)
    time.sleep(LOADING_PERIOD)
    # TODO: we will face with bug if we find a profile that have no followers or following
    try:
        actual_username = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/h1").text
    except:
        actual_username = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/h2").text

    if username == actual_username:
        try:
            followers = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title").replace(',', ''))
        except:
            followers = 0

        try:
            following = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text.replace('following', '').replace(' ', ''))
        except:
            following = 0

        try:
            posts = int(driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").text.replace(',', ''))
        except:
            posts = 0

        last_post_url = get_last_post_link()
        likes, view, content_type, post_date, post_time, link, saving_date, saving_time =  get_post_information(last_post_url)

        return ({KEY_USERNAME: actual_username},
                {KEY_FOLLOWERS: followers},
                {KEY_FOLLOWING: following},
                {KEY_POSTS: posts},
                {KEY_LAST_POST_DATE: post_date},
                {KEY_LAST_POST_TIME: post_time},
                {KEY_LIKES: likes},
                {KEY_VIEWS: view},
                {KEY_LINK: link},
                {KEY_SAVE_DATE: saving_date},
                {KEY_SAVE_TIME: saving_time},
                {KEY_CONTENT: content_type})
    else:
        return None


def get_last_post_information(link):
    """ get last post url and then open it, finally extract date and time"""
    # posts
    # post_url = ""
    # links = driver.find_elements_by_tag_name('a')
    # for link in links:
    #     attr = link.get_attribute('href')
    #     if '/p/' in attr:
    #         post_url = attr
    #         break

    driver.get(link)
    time.sleep(PAGE_INTERACT_PERIOD)
    user_name = driver.find_element_by_xpath(
        "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a").text
    print(user_name)
    post_datetime = driver.find_element_by_xpath(
        "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[2]/a/time").get_attribute('datetime')
    post_date, post_time = post_datetime.split("T")
    post_time = post_time[:len(post_time)-5]

    # date_save = datetime.datetime.now().date()
    # time_save = datetime.datetime.now().now().strftime("%X")
    date_save, time_save = get_current_time_and_date()
    print(post_date, post_time)
    return (post_date, post_time, user_name, link, date_save, time_save)

# ------------------------------------------------------------------------------

def calculate_engagement(likes, views, followers):
    engagement = (((likes+views) / MAX_POSTS) / int(followers)) * 100
    return {KEY_ENGAGEMENT: engagement}

def read_information(file_path):
    return (pd.read_csv(file_path, index_col='username'))

# TODO: we should edit this method, because this method will work just for one file!
def write_to_csv(file_path_dest, information, action):
    global WRITE
    global APPEND
    """ with this method we can convert txt file to cvs file """
    headers = list(information.keys())

    if action == WRITE:
        with open(file_path_dest, 'w', newline='') as csv_file:

            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerow(information)

    elif action == APPEND:
        with open(file_path_dest, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writerow(information)

    else:
        print('write_to_csv() --> unknown action')

def get_current_time_and_date():
    return (datetime.datetime.utcnow().date(), datetime.datetime.utcnow().strftime("%X"))

def strToDatetime(str_date_time):
    datetime_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(str_date_time, datetime_format)

#TODO: DO NOT DELETE THIS - JUST UPDATE THIS ONE!
# def scrape_instagram_profiles(profiles):
#     profiles_count = len(profiles)
#     counter = 1
#     for profile in profiles:
#         print(f'User {counter} of {profiles_count} is in proccessing')
#         profile_information = {}
#         find_profile(profile)
#         followers, posts = get_profile_information()
#         likes, views, analysed_posts = total_likes(MAX_POSTS)
#         engagement = calculate_engagement(
#             likes[KEY_LIKES], views[KEY_VIEWS], followers[KEY_FOLLOWERS])
#         user_information = {KEY_USERNAME: profile}
#         profile_information.update(user_information)
#         profile_information.update(followers)
#         profile_information.update(posts)
#         profile_information.update(likes)
#         profile_information.update(views)
#         profile_information.update(analysed_posts)
#         profile_information.update(engagement)
#         write_information(RESULT_PATH, profile_information)
#         counter += 1

def initial_profile_database(profiles):
    create_folder(APP_FOLDER)

    profiles_count = len(profiles)
    counter = 1

    for profile in profiles:
        print(f'User {counter} of {profiles_count} is in proccessing')
        profile_information = {}
        task_informaion = {}
        actual_username, followers, following, posts, last_post_date, last_post_time, likes, views, link, date_save, time_save, content_type = get_profile_information(profile)

        profile_information.update(actual_username)
        profile_information.update(followers)
        profile_information.update(following)
        profile_information.update(posts)
        profile_information.update(content_type)
        profile_information.update(likes)
        profile_information.update(views)
        profile_information.update(link)
        profile_information.update(last_post_date)
        profile_information.update(last_post_time)
        profile_information.update(date_save)
        profile_information.update(time_save)

        print(f'collected information is \n{profile_information}')

        # remain_time = {KEY_REMAIN_TIME: 
        task_informaion.update(actual_username)
        task_informaion.update(link)
        task_informaion.update(date_save)
        # check_info.update(remain_time)

        if counter == 1:
            write_to_csv(PAGES_INIT_DB, profile_information, WRITE)
            write_to_csv(TASKMANAGER_PATH, task_informaion, WRITE)
        else:
            write_to_csv(PAGES_INIT_DB, profile_information, APPEND)
            write_to_csv(TASKMANAGER_PATH, task_informaion, APPEND)

        counter += 1

    print('INITIAL PROFILE DATABASE finished')


# TODO: UPDATE THIS PLEASE! 
def make_csv_file(profiles):
    ''' here it makes folders by name of each profile name in each folder it makes csv file '''

    for profile in profiles:

        path = CSV_FILE + '\\' + profile
        os.mkdir(path)

        csv_path = path + '\\' + profile + '.csv'

        with open(csv_path, 'w') as file:
            file.write('')

def check_profiles(profiles, PAGES_INIT_DB):
    dicts = {}
    replace = {}
    check_info = {}
    days = 14

    # steps:
    # search profiles that was read from db and then compare with data that in init db

    dtfr = read_information(PAGES_INIT_DB)

    for profile in profiles:
        go_to_profile(profile)

        # followers, following, posts = get_followers_count()

        db_datetime = strToDatetime(dtfr.at[profile, 'last_post_date'] + ' ' + dtfr.at[profile, 'last_post_time'])

        time.sleep(PAGE_INTERACT_PERIOD)
        link = get_last_post_link()
        post_date, post_time, user, link, date_save, time_save = get_last_post_information(link)
        current_post_datetime = strToDatetime(post_date + ' ' + post_time)

        if db_datetime < current_post_datetime:

            print(f'New post detect in {profile} adding to watchlist')

            user_information = {KEY_USERNAME: profile}
            link = {KEY_LINK: link}
            remain_time = {KEY_REMAIN_TIME: days}
            date_save = {KEY_SAVE_DATE: date_save}

            check_info.update(user_information)
            check_info.update(link)
            check_info.update(date_save)
            check_info.update(remain_time)
            print('adding to Taskk_manager')
            task_manager_update(TASKMANAGER_PATH, check_info)
            # data_base updating
            print('data base updating...')
            
            replace_db(profile , PAGES_INIT_DB)
        
        
        else:
            print('nothing detected')


def monitoring(profiles, PAGES_INIT_DB):
    print('Monitoring Started')
    check_profiles(profiles, PAGES_INIT_DB)


def task_manager_expire(path, urls):

    # after 14 days of checking  you should call task_manager_expire with path and old url :))

    df = pd.read_csv(path, index_col='link')

    df2 = df.drop(index=urls)

    df2.to_csv(path)


def task_manager_update(path, information):
    # if a new post detected you should call task_manager_update and pass path and new information :)))

    headers = list(information.keys())

    with open(path, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writerow(information)



def replace_db(profile , pages_init_db):
    dtfr = read_information(pages_init_db)
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
    print(replace_dic)
    df2 = dtfr.at[profile , 'followers'] , dtfr.at[profile , 'following'] , dtfr.at[profile , 'posts'] , dtfr.at[profile , 'content_type'] , dtfr.at[profile , 'likes'] , dtfr.at[profile , 'views'], dtfr.at[profile , 'link'], dtfr.at[profile , 'last_post_date'], dtfr.at[profile , 'last_post_time'], dtfr.at[profile , 'save_date'], dtfr.at[profile , 'save_time']
    for i,j in zip(KEYS,df2):
        dicts[i]=j

    df3 = dtfr.replace({dicts['followers'] : replace_dic[KEY_FOLLOWERS] , dicts['following'] : replace_dic[KEY_FOLLOWING] , dicts['posts'] : replace_dic[KEY_POSTS] , dicts['content_type'] : replace_dic[KEY_CONTENT] , dicts['likes'] : replace_dic[KEY_LIKES] , dicts['views'] : replace_dic[KEY_VIEWS] , dicts['link'] : replace_dic[KEY_LINK] , dicts['last_post_date'] : replace_dic[KEY_LAST_POST_DATE] , dicts['last_post_time'] : replace_dic[KEY_LAST_POST_TIME] , dicts['save_date'] : replace_dic[KEY_SAVE_DATE] , dicts['save_time'] : replace_dic[KEY_SAVE_TIME]})
    print(df3)
    df3.to_csv(pages_init_db)



def strToDatetime_csv(str_date_time):
    
    # this def read times in csv and change format with this model month/day/year to year/month/day
    
    datetime_format = "%m/%d/%Y"
    return datetime.datetime.strptime(str_date_time, datetime_format).date()

def check_time(task_path):
    # this def , find save_date any profile then calculate time for task_manager and each user_csv, after calculate must remove link from task_manager and stop calculation of user_csv
    date_now = datetime.datetime.now().date()
    
    for profile in profiles:
        df = pd.read_csv(task_path , index_col = 'username')
        df2 = df.at[profile , 'save_date']
        df2 = strToDatetime_csv(df2)
    
    result = str(abs(date_now - df2)).split(' ')
    time = int(result[0])
     
    if b >= 14 :
        print("remove link")
    else:
        print("continue checking")


# Main ________________________________________________
# we will sign into instagram and make environment ready to run script
def run_bot():
    """ this method will initialize bot """
    init_instagram()
    initial_profile_database(profiles)

    # if not INIT_DATABASE_STATUS:
    # init a database of users information
    # keep eyes on profiles that post new content

    monitoring(profiles, PAGES_INIT_DB)
    # time.sleep(WATCHLIST_PERIOD)


# TODO: WARNING - edit here in production
if not DEBUG:
    profiles = get_usernames(PROFILES_USERNAME_DB)
else:
    profiles = get_usernames(PROFILES_USERNAME_DB)[:1]

run_bot()



