# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 18:38:26 2021

@author : Amirhosein syh
"""

import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date

import time, datetime
import json, csv

import pandas as pd

# config:
DRIVER_PATH = os.path.dirname(__file__) + r"/chromedriver"
driver = webdriver.Chrome(DRIVER_PATH)

USERNAME = 'annonymous_test'
PASSWORD = 'this is a test 123'

DEBUG = True
COOKIES = True
INIT_DATABASE_STATUS = False

CSV_FILE = os.path.dirname(__file__)
PROFILES_USERNAME_DB = os.path.dirname(__file__) + r"/user_profiles_db.txt"
PAGES_INIT_DB = os.path.dirname(__file__) + r"/pages_init_db.csv"
WATCHLIST_DB = os.path.dirname(__file__) + r"/watchlist_db.txt"
USER_INFORMATIONS = os.path.dirname(__file__) + r"/user_basic_informations.txt"
RESULT_PATH = os.path.dirname(__file__) + r"/result.txt"
TASKMANAGER_PATH = os.path.dirname(__file__) + r"/task_manager.csv"

LOADING_PERIOD = 15
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

def new_tab(url):
    driver.execute_script(f'''window.open("{url}","_blank");''')

def init_instagram():
    """ we will login to instagram and make our bot ready """
    driver.get("https://www.instagram.com/")
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
    # searchbox    
    time.sleep(LOADING_PERIOD)
    searchbox = driver.find_element_by_css_selector("input[placeholder='Search']")
    searchbox.clear()
    searchbox.send_keys(username)
    time.sleep(PAGE_INTERACT_PERIOD)
    searchbox.send_keys(Keys.ENTER)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(PAGE_INTERACT_PERIOD)
    
def get_profile_information():
    # extraction followers, posts
    time.sleep(LOADING_PERIOD)
    
    followers = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title").replace(',', '')) 
    
    try:
        
       following = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text.replace('following', '').replace(' ', ''))
    
    except:
    
        following = 0
    
    posts = int(driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").text.replace(',',''))
    
    # open last post and get time
    last_post_date, last_post_time, user, link, date_save, time_save = get_last_post_information()
    link = ''.join(link)
    likes, video_inf, content_type = total_likes(1)

    return ({KEY_FOLLOWERS : followers}, {KEY_FOLLOWING : following}, {KEY_POSTS : posts}, 
            {KEY_LAST_POST_DATE : last_post_date}, {KEY_LAST_POST_TIME : last_post_time},
            {KEY_LIKES : likes}, {KEY_VIEWS : video_inf }, {KEY_LINK : link}, {KEY_SAVE_DATE : date_save} , 
            {KEY_SAVE_TIME: time_save}, {KEY_CONTENT : content_type })




def get_last_post_information():
    """ get last post url and then open it, finally extract date and time"""    
    #posts
    post_url = ""
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        attr = link.get_attribute('href')
        if '/p/' in attr:
            post_url = attr
            break
        
    driver.get(post_url)
    time.sleep(PAGE_INTERACT_PERIOD)       
    user_name = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a").text
    print(user_name)
    post_datetime = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[2]/a/time").get_attribute('datetime')
    post_date, post_time = post_datetime.split("T")
    post_time = post_time[:len(post_time)-5]
    
    date_save = datetime.datetime.now().date()
    time_save = datetime.datetime.now().now().strftime("%X")
    # c = str(datetime.datetime.now())
    # date_save , time_save = c.split(' ')
    # time_save = time_save[:-7]
    print(post_date, post_time)
    # driver.close()
    return (post_date, post_time, user_name, post_url, date_save, time_save)


# ------------------------------------------------------------------------------
def total_likes(MAX_POSTS):

    if MAX_POSTS >= 5:
        # scroll
        scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        match=False
        while(match==False):
            last_count = scrolldown
            time.sleep(LOADING_PERIOD)
            scrolldown = ("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
            if last_count==scrolldown:
                match=True 
    #posts
    posts_links = []
    links = driver.find_elements_by_tag_name('a')
    
    for link in links:
        attr = link.get_attribute('href')
        if '/p/' in attr:
            posts_links.append(attr)
            if len(posts_links) == MAX_POSTS:
                break
    
    #get videos and images
    counter = 1
    for post in posts_links:
        print(f'Post {counter} of {len(posts_links)} is in proccessing')
        driver.get(post)
        time.sleep(PAGE_INTERACT_PERIOD)
        try:
            likes = (((driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/a/span").text).replace(',','')))
            view = 0 
        except:
            driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span").click()
            time.sleep(PAGE_INTERACT_PERIOD)
            likes = (((driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div[4]/span").text).replace(',','')))
            view = (((driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/span/span").text).replace(',','')))
            # print(view)
            
        # sum_likes = sum(list(map(int,likes)))
        # sum_view = sum(list(map(int,view)))
        counter += 1
        if int(view) > 0 :
            content_type = 'video'
        else:
            content_type = 'image'
            
    print(int(view), int(likes))  
    # return dictionary 
    # return ({KEY_LIKES : sum_likes}, {KEY_VIEWS : sum_view}, {KEY_ANALYSED_POSTS: len(posts_links)})
    return (int(likes), int(view), content_type)

def calculate_engagement(likes, views, followers):
    engagement = (((likes+views) / MAX_POSTS) / int(followers)) * 100
    return {KEY_ENGAGEMENT : engagement}

# we do not need this anymore
def write_information(file_path, information):
    global CLEANED_FILE
    if not CLEANED_FILE:
        print('Cleaning file for the first time')
        open(file_path, 'w').close()
        CLEANED_FILE = True
    with open(file_path, 'a') as file:
        print('Saving information in file')
        file.write(json.dumps(information))
        file.write("\n")
        

def read_information(file_path):
    
    df = pd.read_csv(file_path , index_col = 'username' )

    return (df)

# TODO: we should edit this method, because this method will work just for one file!
def write_to_csv(file_path_dest, information, action):
    global WRITE
    global APPEND
    """ with this method we can convert txt file to cvs file """
    headers = list(information.keys())
    
    if action == WRITE:
        with open(file_path_dest, 'w', newline= '') as csv_file:   

            writer = csv.DictWriter(csv_file,fieldnames = headers )
            writer.writeheader()  
            writer.writerow(information) 
        
    elif action == APPEND:
        with open(file_path_dest, 'a', newline= '') as csv_file:       
            writer = csv.DictWriter(csv_file,fieldnames = headers )
            writer.writerow(information)
        
    else:
        print('write_to_csv() --> unknown action')
    
  
           

def strToDatetime(str_date_time):
    datetime_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(str_date_time, datetime_format)
    

def scrape_instagram_profiles(profiles):
    profiles_count = len(profiles)
    counter = 1
    for profile in profiles:
        print(f'User {counter} of {profiles_count} is in proccessing')
        profile_information = {}
        find_profile(profile)
        followers, posts = get_profile_information()
        likes, views, analysed_posts = total_likes(MAX_POSTS)
        engagement = calculate_engagement(likes[KEY_LIKES], views[KEY_VIEWS], followers[KEY_FOLLOWERS])
        user_information = {KEY_USERNAME : profile}
        profile_information.update(user_information)
        profile_information.update(followers)
        profile_information.update(posts)
        profile_information.update(likes)
        profile_information.update(views)
        profile_information.update(analysed_posts)
        profile_information.update(engagement)
        write_information(RESULT_PATH, profile_information)
        counter += 1


def initial_profile_database(profiles):
    
    profiles_count = len(profiles)
    
    days = 14
    counter = 1
    
    for profile in profiles:
        
        print(f'User {counter} of {profiles_count} is in proccessing')
        profile_information = {}
        #check_info makes dictionary with username , link , date and days of remaining for checking 
        path = CSV_FILE  +'\\' + profile 

        check_info = {}
        find_profile(profile)
        
        followers, following, posts, last_post_date, last_post_time, likes, views, link, date_save, time_save,content_type = get_profile_information()
        
        user_information = {KEY_USERNAME : profile}
        profile_information.update(user_information)
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
        
        remain_time = {KEY_REMAIN_TIME : days}
        check_info.update(user_information)
        check_info.update(link)
        check_info.update(date_save)
        check_info.update(remain_time)
        
        if counter == 1:    
            write_to_csv(PAGES_INIT_DB, profile_information, WRITE)
            write_to_csv(TASKMANAGER_PATH, check_info, WRITE)
        else:
            write_to_csv(PAGES_INIT_DB, profile_information, APPEND)
            write_to_csv(TASKMANAGER_PATH, check_info, APPEND)

        counter += 1
                
    
    print('INITIAL PROFILE DATABASE finished')
    
    
    
def make_csv_file (profiles):
    ''' here it makes folders by name of each profile name in each folder it makes csv file '''

    for profile in profiles:
                
        path = CSV_FILE  +'\\' + profile 
        os.mkdir(path)
        
        csv_path = path + '\\' + profile + '.csv'
        
        with open(csv_path,'w') as file:
            file.write('')
            

def add_to_watchlist(username, last_post_date, last_post_time, likes, views, link, date_save, time_save):
    
    # open watchlist db and then save information into it
    
    information = {KEY_USERNAME: username, KEY_LAST_POST_DATE: last_post_date, KEY_LAST_POST_TIME: last_post_time,KEY_LIKES:likes,KEY_VIEWS:views, KEY_LINK:link,KEY_SAVE_DATE:date_save, KEY_SAVE_TIME: time_save}
    
    with open(WATCHLIST_DB, 'a') as file:
    
        print('Saving information in watchlist file')
        
        file.write(json.dumps(information))
        file.write("\n")
        
        
def get_followers_count():
    followers = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title").replace(',', '')) 
    try:
        
       following = (driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text.replace('following', '').replace(' ', ''))
    
    except:
    
        following = 0
    
    posts = int(driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").text.replace(',',''))
    
    return {KEY_FOLLOWERS : followers}, {KEY_FOLLOWING : following}, {KEY_POSTS : posts}
    

def check_profiles(profiles, PAGES_INIT_DB):
    
    check_info = {}
    days = 14
    
    # steps:
    # search profiles that was read from db and then compare with data that in init db
    
    dtfr = read_information(PAGES_INIT_DB)


    for profile in profiles:
    
        find_profile(profile)
        
        followers, following, posts = get_followers_count()

        db_datetime = strToDatetime(dtfr.at[profile , 'last_post_date'] + ' ' + dtfr.at[profile, 'last_post_time'])
        
        time.sleep(PAGE_INTERACT_PERIOD)
        
        post_date, post_time , user, link, date_save, time_save = get_last_post_information()
        current_post_datetime = strToDatetime(post_date + ' ' + post_time)
    
        if db_datetime < current_post_datetime:
    
            print(f'New post detect in {profile} adding to watchlist')
            
            user_information = {KEY_USERNAME : profile}
            link = {KEY_LINK : link}
            remain_time = {KEY_REMAIN_TIME : days}
            date_save = {KEY_SAVE_DATE : date_save}
    
            check_info.update(user_information)
            check_info.update(link)
            check_info.update(date_save)
            check_info.update(remain_time)
            print('adding to Taskk_manager')
            task_manager_update(TASKMANAGER_PATH, check_info)
            #data_base updating
            print('data base updating...')
            
            # dtfr =dtfr.drop(profile, axis=0)            
            # df2 = {'username': profile,'followers': followers.values() , 'following' : following.values() , 'posts': posts.values() , 'link': link.values(), 'save_date': date_save.values(),'save_time':time_save}        
            # dtfr = dtfr.append(df2, ignore_index = True)
            # print(dtfr)
            # time.sleep(3)
            # os.remove(PAGES_INIT_DB) 
            # dtfr.to_csv(PAGES_INIT_DB)
        else:
            print('nothing detected')
        

        
    

def monitoring(profiles, PAGES_INIT_DB):
    
    print('Monitoring Started')
    check_profiles(profiles, PAGES_INIT_DB)
    


def task_manager_expire(path, urls):
    
    #after 14 days of checking  you should call task_manager_expire with path and old url :))
    
    df = pd.read_csv(path , index_col = 'link' )

    df2 = df.drop(index= urls)
    
    df2.to_csv(path)



def task_manager_update(path, information):
    #if a new post detected you should call task_manager_update and pass path and new information :)))
    
    
    headers = list(information.keys())
    
    with open(path, 'a', newline= '') as csv_file:       
        writer = csv.DictWriter(csv_file,fieldnames = headers )
        writer.writerow(information)


        

# Main ________________________________________________
# we will sign into instagram and make environment ready to run script
def run_bot():
    
    """ this method will initialize bot """
    # step A. connect to instagram and create file which contains user followers, username, last post time
    # connect to instagram and login to account
    init_instagram()
    initial_profile_database(profiles)
    # make_csv_file(profiles)
    
    # if not INIT_DATABASE_STATUS:
        # init a database of users information
        # keep eyes on profiles that post new content


    monitoring(profiles, PAGES_INIT_DB)        
        # time.sleep(WATCHLIST_PERIOD)

# TODO: WARNING - edit here in production
if not DEBUG:    
    profiles = get_usernames(PROFILES_USERNAME_DB)
else: 
    profiles = get_usernames(PROFILES_USERNAME_DB)[98:99]



run_bot()
