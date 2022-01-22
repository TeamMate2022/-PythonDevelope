# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 18:38:26 2021

@author : Amirhosein syh
"""

from http import cookies
import os
from typing import Counter

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import date

import time
import datetime
import json
import csv

import pandas as pd
import pickle

# config:
DRIVER_PATH = os.path.dirname(__file__) + r"/chromedriver"
driver = webdriver.Chrome(DRIVER_PATH)
driver.maximize_window()
tabs = []

INSTAGRAM = 'https://www.instagram.com/'
# USERNAME = 'annonymous_test'
# PASSWORD = 'this is a test 123'

USERNAME = "tes_tthis"
PASSWORD = "this is a test 123"

DEBUG = True
COOKIES_DIALOG = True
INIT_DATABASE_STATUS = False

USE_SAVED_COOKIES = True

APP_FOLDER = r'/instascraper data'

CSV_FILE = os.path.dirname(__file__) + APP_FOLDER
PROFILES_USERNAME_DB = os.path.dirname(__file__) + r"/user_profiles_db.txt"
PAGES_INIT_DB = os.path.dirname(__file__)+ APP_FOLDER + r"/pages_init_db.csv"
WATCHLIST_DB = os.path.dirname(__file__) + APP_FOLDER+ r"/watchlist_db.txt"
USER_INFORMATIONS = os.path.dirname(__file__) + APP_FOLDER + r"/user_basic_informations.txt"
RESULT_PATH = os.path.dirname(__file__) + APP_FOLDER + r"/result.txt"
TASKMANAGER_PATH = os.path.dirname(__file__) + APP_FOLDER + r"/task_manager.csv"
COOKIES_FILE = os.path.dirname(__file__) + APP_FOLDER + r'/chrome_cookies.pkl'

LOADING_PERIOD = 12
PAGE_INTERACT_PERIOD = 4
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

def app_log(method_name, message):
    print(f'INSTASCRAPER APP -- we are in "{method_name}". \n\t message: {message} \n')

def create_app_folder():
    try:
        app_log('create_app_folder','Try to create a folder for the app')
        os.makedirs(os.getcwd() + APP_FOLDER)
    except:
        app_log('create_app_folder', 'Application folder exists!')

def retrive_saved_cookies():
    app_log('retrive_saved_cookies', 'Retriving cookies from saved file')
    return pickle.load(open(COOKIES_FILE, 'rb'))

def save_cookies():
    app_log('save_cookies', 'Saving current cookies')
    pickle.dump(driver.get_cookies(), open(COOKIES_FILE, 'wb'))
    
def manage_cookies():
    try:
        for cookie in retrive_saved_cookies():
            driver.get(INSTAGRAM)
            driver.add_cookie(cookie)
        return True
    except:
        app_log('manage_cookies', 'No cookies file found. Starting in fresh mode!')
        return False

def login():
    create_app_folder()
    
    using_cached_cookies = False
    if USE_SAVED_COOKIES:
        using_cached_cookies = manage_cookies()

        
    if using_cached_cookies:
        app_log('login', 'using cached cookies')
    else:
        driver.get(INSTAGRAM)
        
        # accept cookies:
        if COOKIES_DIALOG:
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
        # save login info?
        time.sleep(PAGE_INTERACT_PERIOD)
        driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        
    save_cookies()
    

def init_instagram():
    """ we will login to instagram and make our bot ready """
    login()
    # turn off notif
    time.sleep(PAGE_INTERACT_PERIOD)
    driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

# --------------------- TAB MANAGER SECTION
# if you want to findout tab id of specific url, you can use this method
def find_tab_id(tab_link):
    for tab in tabs:
        if tab['tab_link'] == tab_link:
            return tab['tab_id']

# open new tab and open links - save tab information to a list
def open_tabs(links):
    for link in links:
        tab_information = {}
        # first of all open a new tab
        driver.execute_script("window.open('');")
        # switch to new tab
        driver.switch_to.window(driver.window_handles[(len(driver.window_handles)-1)])
        driver.get(link)
        tab_information['tab_id'] = len(driver.window_handles) - 1
        tab_information['tab_link'] = link
        print(tab_information)
        tabs.append(tab_information)
    return tabs

# refresh specific tab
def refresh_tab(tab_id):
    driver.switch_to.window(driver.window_handles[tab_id])
    driver.refresh()
    time.sleep(2)

# switch to specific tab
def switch_to_tab(tab_id):
    driver.switch_to.window(driver.window_handles[tab_id])
    time.sleep(1)
    return True

def close_tab(tab_id):
    driver.switch_to.window(driver.window_handles[tab_id])
    time.sleep(2)
    driver.close()
    if (len(driver.window_handles)) <= 1:
        driver.switch_to.window(driver.window_handles[tab_id]-1)

# def close_tab(tab_link):
#     for tab in tabs:
#         if tab['tab_link'] == tab_link:
#             print(tab_link)
#             driver.switch_to.window(driver.window_handles[tab['tab_id']])
#             time.sleep(2)
#             driver.close()
#             if (len(driver.window_handles)) <= 1:
#                 driver.switch_to.window(driver.window_handles[tab['tab_id']]-1)    

# we will manage our tabs here
def tab_manager(links):
    tabs = []
    # open links in new tabs:
    tabs = open_tabs(links)

    time.sleep(2)

    # refresh_tabs(tabs_list)
    for tab in tabs:
        if switch_to_tab(tab['tab_id']):
            print(f"Refreshing page number {tab['tab_id']}")
            refresh_tab(tab['tab_id'])

    # print(find_tab_id[tabs[0]['tab_link']]
    close_tab(tabs[1]['tab_id'])
    # close_tab(tabs[1]["tab_link"])

# --------------------- TAB MANAGER SECTION

def get_usernames(PROFILES_USERNAME_DB):
    """ this method will read usernames from user_profiles file"""
    return open(PROFILES_USERNAME_DB, 'r').read().split('\n')

def find_profile(username):
    app_log('find_profile', f'start to search for {username}')
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
    app_log('go_to_profile', f"try to open page by it's URL")
    time.sleep(PAGE_INTERACT_PERIOD)
    driver.get(INSTAGRAM + username)

def get_last_post_link():
    app_log('get_last_post_link', 'want to get last post link')
    post_url = ""
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        attr = link.get_attribute('href')
        if '/p/' in attr:
            post_url = attr
            break
    app_log('get_last_post_link', f'last post url "{post_url}"')
    
    return post_url

def get_post_information(link):
    """ with this method we can collect post information by it's link"""
    app_log('get_post_information', f'try to open "{link}" and collect data')
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

    #TODO: we should fix this bug later!
    # try:
    #     try:
    #         likes = (((driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/a')))).text
    #         view = 0
    #     except:    
    #         likes = (((driver.find_element_by_xpath(
    #             "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/a/span").text).replace(',', '')))
    #         view = 0
    # except:
    #     try:
    #         tag_name = '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[1]/div/div/div/div/div/video'.tag_name
    #     except:
    #         tag_name = ""
            
    #     print(tag_name)
    #     try:
    #         if tag_name == 'video':
    #             driver.find_element_by_xpath(
    #                 "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span").click()
    #             # time.sleep(PAGE_INTERACT_PERIOD)
    #             likes = (((driver.find_element_by_xpath(
    #                 "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div[4]/span").text).replace(',', '')))
    #             view = (((driver.find_element_by_xpath(
    #                 "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span/span").text).replace(',', '')))
    #     except:
    #         likes = 0
    #         view = 0

    
    post_datetime = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[2]/a/time").get_attribute('datetime')
    post_date, post_time = post_datetime.split("T")
    post_time = post_time[:len(post_time)-5]
    saving_date, saving_time = get_current_time_and_date()

    if int(view) > 0:
        content_type = 'video'
    else:
        content_type = 'image'

    return (int(likes), int(view), content_type, post_date, post_time, link, saving_date, saving_time)


def get_profile_information(username):
    app_log('get_profile_information', f'start to collect data from "{username}"')
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
    app_log('get_last_post_information', '')
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

def strToDatetime_csv(str_date_time):
    # this def read times in csv and change it's format to this format month/day/year to year/month/day
    datetime_format = "%m/%d/%Y"
    return datetime.datetime.strptime(str_date_time, datetime_format).date()

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
    
    profiles_count = len(profiles)
    counter = 1
    
    for profile in profiles:
        app_log('initial_profile_database', f'User {counter} of {profiles_count} is in proccessing')
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

        print(f'collected information from "{profile}" is \n{profile_information}')

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

    app_log('initial_profile_database', 'database created successfully')


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
    app_log("check_profiles", 'checking profiles to find new post')
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
            # app_log("check_profiles", f'New post detected in {profile}. Adding "{profile}" to watchlist')
            print(f'New post detected in {profile}. Adding "{profile}" to watchlist')

            user_information = {KEY_USERNAME: profile}
            link = {KEY_LINK: link}
            remain_time = {KEY_REMAIN_TIME: days}
            date_save = {KEY_SAVE_DATE: date_save}

            check_info.update(user_information)
            check_info.update(link)
            check_info.update(date_save)
            check_info.update(remain_time)
            print('adding "{profile} to task_manager')
            task_manager_update(TASKMANAGER_PATH, check_info)
            # data_base updating
            print('updating database...')
            
            replace_db(profile , PAGES_INIT_DB)
        
        
        else:
            print('nothing detected')


def monitoring(profiles, PAGES_INIT_DB):
    app_log('monitoring', 'Monitoring Started!')
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
    app_log("run_bot", "Let the show begin!")
    # init_instagram()
    login()
    initial_profile_database(profiles)

    # if not INIT_DATABASE_STATUS:
    # init a database of users information
    # keep eyes on profiles that post new content

    # monitoring(profiles, PAGES_INIT_DB)
    # time.sleep(WATCHLIST_PERIOD)


# TODO: WARNING - edit here in production
if not DEBUG:
    profiles = get_usernames(PROFILES_USERNAME_DB)
else:
    profiles = get_usernames(PROFILES_USERNAME_DB)[:1]

run_bot()
