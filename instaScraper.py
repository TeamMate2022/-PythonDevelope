# -*- coding: utf-8 -*-
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import datetime
import csv

import pandas as pd
import pickle

# config:
DRIVER_PATH = os.path.dirname(__file__) + r"/chromedriver"
driver = webdriver.Chrome(DRIVER_PATH)
driver.maximize_window()

INSTAGRAM = 'https://www.instagram.com/'
# USERNAME = 'annonymous_test'
# PASSWORD = 'this is a test 123'

USERNAME = "tes_tthis"
PASSWORD = "this is a test 12"

DEBUG = True
COOKIES_DIALOG = True
INIT_DATABASE_STATUS = False

USE_SAVED_COOKIES = True

APP_FOLDER = r'/instascraper data'

list_link = []

CSV_FILE = os.path.dirname(__file__) + APP_FOLDER + r"/{}"
PROFILES_USERNAME_DB = os.path.dirname(__file__) + r"/user_profiles_db.txt"
ALL_USER_INFORMATIONS = os.path.dirname(__file__) + APP_FOLDER + r"/All-Users-information.csv"
WATCHLIST_DB = os.path.dirname(__file__) + APP_FOLDER + r"/watchlist_db.txt"
USER_INFORMATIONS = os.path.dirname(
    __file__) + APP_FOLDER + r"/user_basic_informations.txt"
LIST_OF_LINKS = os.path.dirname(
    __file__) + APP_FOLDER + r"/list of links.txt"
RESULT_PATH = os.path.dirname(__file__) + APP_FOLDER + r"/result.txt"
TASK_LIST_CSV = os.path.dirname(
    __file__) + APP_FOLDER + r"/Tasks-List.csv"
COOKIES_FILE = os.path.dirname(__file__) + APP_FOLDER + r'/chrome-cookies.pkl'

LOADING_PERIOD = 13
PAGE_INTERACT_PERIOD = 5
MAX_POSTS = 5

WATCHLIST_PERIOD = 60
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
KEY_POST_DATE = "post_date"
KEY_POST_TIME = "post_time"
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
NEW = 'new_post'


def app_log(method_name, message):
    print(
        f'INSTASCRAPER APP -- we are in "{method_name}". \n\t message: {message} \n')

def create_app_folder():
    try:
        app_log('create_app_folder', 'Try to create a folder for the app')
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
            driver.find_element_by_xpath(
                "//button[contains(text(), 'Accept All')]").click()

        # login
        time.sleep(LOADING_PERIOD)
        username = driver.find_element_by_css_selector(
            "input[name='username']")
        password = driver.find_element_by_css_selector(
            "input[name='password']")
        username.clear()
        password.clear()
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        driver.find_element_by_css_selector("button[type='submit']").click()
        time.sleep(PAGE_INTERACT_PERIOD)
        # save login info?
        time.sleep(PAGE_INTERACT_PERIOD)
        driver.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]").click()

    save_cookies()


def init_instagram():
    """ we will login to instagram and make our bot ready """
    login()
    # turn off notif
    time.sleep(PAGE_INTERACT_PERIOD)
    driver.find_element_by_xpath(
        "//button[contains(text(), 'Not Now')]").click()

def get_usernames(PROFILES_USERNAME_DB):
    """ this method will read usernames from user_profiles file"""
    return open(PROFILES_USERNAME_DB, 'r').read().split('\n')


def find_profile(username):
    app_log('find_profile', f'start to search for {username}')
    # searchbox
    time.sleep(LOADING_PERIOD)
    searchbox = driver.find_element_by_css_selector(
        "input[placeholder='Search']")
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
    user_name = driver.find_element_by_xpath(
        "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a").text
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

    # TODO: we should fix this bug later!
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

    post_datetime = driver.find_element_by_xpath(
        "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[2]/a/time").get_attribute('datetime')
    post_date, post_time = post_datetime.split("T")
    post_time = post_time[:len(post_time)-5]
    saving_date, saving_time = get_current_time_and_date()

    if int(view) > 0:
        content_type = 'video'
    else:
        content_type = 'image'

    return (user_name, int(likes), int(view), content_type, post_date, post_time, link, saving_date, saving_time)

def get_profile_information(username):
    go_to_profile(username)
    time.sleep(LOADING_PERIOD)
    # TODO: we will face with bug if we find a profile that have no followers or following
    try:
        actual_username = driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/div/header/section/div[1]/h1").text
    except:
        actual_username = driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/div/header/section/div[1]/h2").text

    if username == actual_username:
        try:
            followers = (driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title").replace(',', ''))
        except:
            followers = 0

        try:
            following = (driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text.replace('following', '').replace(' ', ''))
        except:
            following = 0

        try:
            posts = int(driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").text.replace(',', ''))
        except:
            posts = 0

        last_post_url = get_last_post_link()
        saving_date, saving_time = get_current_time_and_date()

        return ({KEY_USERNAME: actual_username},
                {KEY_FOLLOWERS: followers},
                {KEY_FOLLOWING: following},
                {KEY_POSTS: posts},
                {KEY_LINK: last_post_url},
                {KEY_SAVE_DATE: saving_date},
                {KEY_SAVE_TIME: saving_time})
    else:
        return None

# TODO: EDIT THIS METHOD LATER
def get_profile_and_last_post_information(username):
    app_log('get_profile_and_last_post_information',
            f'start to collect data from "{username}"')
    # find_profile(username)
    go_to_profile(username)
    time.sleep(LOADING_PERIOD)
    # TODO: we will face with bug if we find a profile that have no followers or following
    try:
        actual_username = driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/div/header/section/div[1]/h1").text
    except:
        actual_username = driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/div/header/section/div[1]/h2").text

    if username == actual_username:
        try:
            followers = (driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title").replace(',', ''))
        except:
            followers = 0

        try:
            following = (driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text.replace('following', '').replace(' ', ''))
        except:
            following = 0

        try:
            posts = int(driver.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").text.replace(',', ''))
        except:
            posts = 0

        last_post_url = get_last_post_link()
        user, likes, view, content_type, post_date, post_time, link, saving_date, saving_time = get_post_information(
            last_post_url)

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
    app_log('get_last_post_information', '')
    driver.get(link)
    time.sleep(PAGE_INTERACT_PERIOD)
    user_name = driver.find_element_by_xpath(
        "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/span/a").text
    # print(user_name)
    post_datetime = driver.find_element_by_xpath(
        "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[2]/a/time").get_attribute('datetime')
    post_date, post_time = post_datetime.split("T")
    post_time = post_time[:len(post_time)-5]

    date_save, time_save = get_current_time_and_date()
    app_log('get_last_post_information',
            f'{post_date, post_time, user_name, link, date_save, time_save}')
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
        app_log('write_to_csv', 'unknown action')

def save_post_information(user, post_information, action):
    user_folder_path = make_user_folder(user)
    post_link = post_information[KEY_LINK].split('/')[4]
    post_path = user_folder_path + r'/{}.csv'.format(post_link)
    write_to_csv(post_path, post_information, action)

def save_profile_information(username, profile_information, action):
    user_folder_path = make_user_folder(username)
    user_information_csv = user_folder_path + r'/{}--PageInformation.csv'.format(username)
    write_to_csv(user_information_csv, profile_information, action)

def save_to_db():
    pass

def save_to_task_manager():
    pass


def get_current_time_and_date():
    return (datetime.datetime.utcnow().date(), datetime.datetime.utcnow().strftime("%X"))


def strToDatetime(str_date_time):
    datetime_format = "%Y-%m-%d %H:%M:%S"
    # datetime_format = "%Y-%M-%d"
    return datetime.datetime.strptime(str_date_time, datetime_format)


def strToDatetime_csv(str_date_time):
    # this def read times in csv and change format with this model month/day/year to year/month/day
    try:
        datetime_format = "%Y-%M-%d"
        csv_time = datetime.datetime.strptime(
            str_date_time, datetime_format).date()
    except:
        datetime_format = "%m/%d/%Y"
        csv_time = datetime.datetime.strptime(
            str_date_time, datetime_format).date()

    # print(csv_time)
    return csv_time


def initial_profile_database(users):

    profiles_count = len(users)

    for index, username in enumerate(users):

        app_log('initial_profile_database',
                f'User {index+1} of {profiles_count} is in proccessing')  

        profile_information = dict()
        post_information = dict()
        task = dict()
        
        actual_username, followers, following, posts, last_post_date, last_post_time, \
         likes, views, link, date_save, time_save, content_type = get_profile_and_last_post_information(username)

        username = actual_username[KEY_USERNAME]
         
        profile_information.update(actual_username)
        profile_information.update(followers)
        profile_information.update(following)
        profile_information.update(posts)
        profile_information.update(link)
        profile_information.update(date_save)
        profile_information.update(time_save)

        # profile_information.update(content_type)
        # profile_information.update(likes)
        # profile_information.update(views)
        # profile_information.update(last_post_date)
        # profile_information.update(last_post_time)
        # profile_information.update(date_save)
        # profile_information.update(time_save)

        post_information.update(link)
        post_information.update(content_type)
        post_information.update(likes)
        post_information.update(views)
        post_information.update(last_post_date)
        post_information.update(last_post_time)
        post_information.update(date_save)
        post_information.update(time_save)

        
        app_log('initial_profile_databse',f'collected information from "{username}" is \n{profile_information}')
        
        # task list csv item:
        task.update(actual_username)
        task.update(link)
        task.update(date_save)
        task.update({KEY_REMAIN_TIME: 14})

        if index == 0:
            write_to_csv(ALL_USER_INFORMATIONS, profile_information, WRITE)
            write_to_csv(TASK_LIST_CSV, task, WRITE)
            
        else:
            write_to_csv(ALL_USER_INFORMATIONS, profile_information, APPEND)
            write_to_csv(TASK_LIST_CSV, task, APPEND)


        # save user information and last post information in user folder
        save_profile_information(username, profile_information, WRITE)
        save_post_information(username, post_information, WRITE) 

    app_log('initial_profile_database', 'informations saved successfully')



def make_user_folder(username):
    try:
        path = CSV_FILE.format(username)
        os.mkdir(path)
        return path
    except FileExistsError:
        app_log('make_csv_file', 'File exists')
        return CSV_FILE.format(username)


def add_new_row(profile_info, action):
    folder_path = CSV_FILE.format(profile_info[KEY_USERNAME])
    
    print(profile_info)
    
    
    # csv_path = folder_path + r'/{}.csv'.format(profile_info[KEY_LINK])   
    
    # link_list = profile_info[KEY_LINK].split('/')
    # new_link = ' '.join(link_list).split()
    
    csv_name = profile_info[KEY_LINK].split('/')[4]
    csv_path = folder_path + r'/{}.csv'.format(csv_name)
    
    # url_path = path + '\\' + new_link[-1] + '.csv'
    
    headers = ['url']
    # try:
    #     if os.stat(csv_path).st_size == 0:
    #         with open(csv_path, 'w', newline='') as csv_file:
    #             writer = csv.DictWriter(csv_file, fieldnames=headers)
    #             writer.writeheader()
    #             writer.writerow({'url': profile_info[KEY_LINK]})
                
    #     elif action == NEW:
    #         with open(csv_path, 'a', newline='') as csv_file:
    #             writer = csv.DictWriter(csv_file, fieldnames=headers)
    #             # writer.writeheader()
    #             writer.writerow({'url': profile_info[KEY_LINK]})

    # except FileNotFoundError:
    #     with open(csv_path, 'w', newline='') as csv_file:
    #         writer = csv.DictWriter(csv_file, fieldnames=headers)
    #         writer.writeheader()
    #         writer.writerow({'url': profile_info[KEY_LINK]})

    # try:
    #     if os.stat(url_path).st_size == 0:
    #         with open(url_path, 'w', newline='') as file:
    #             header = list(profile_info.keys())
    #             writer = csv.DictWriter(file, fieldnames=header)
    #             writer.writeheader()
    #             writer.writerow(profile_info)

    #     else:
    #         with open(url_path, "a", newline='') as file:
    #             header = list(profile_info.keys())
    #             # print(header)
    #             writer = csv.DictWriter(file, fieldnames=header)
    #             # writer.writeheader()
    #             writer.writerow(profile_info)
                
    # except FileNotFoundError:
    #     with open(url_path, 'w', newline='') as file:
    #         header = list(profile_info.keys())
    #         writer = csv.DictWriter(file, fieldnames=header)
    #         writer.writeheader()
    #         writer.writerow(profile_info)


def update_info(list_links):
    list_links = list(set(list_links))
    for link in list_links:
        csv_information = {}
        driver.get(link)
        username, likes, view, content_type, post_date, post_time, link, saving_date, saving_time = get_post_information(
            link)

        actual_username = {KEY_USERNAME: username}
        likes = {KEY_LIKES: likes}
        view = {KEY_VIEWS: view}
        link = {KEY_LINK: link}
        content_type = {KEY_CONTENT: content_type}

        csv_information.update(actual_username)
        csv_information.update(link)
        csv_information.update(likes)
        csv_information.update(view)
        csv_information.update(content_type)
        date, time_n = get_current_time_and_date()
        csv_information.update({'time': time_n})

        add_new_row(csv_information, WRITE)

        app_log('update_info',
                f'updating likes & views of this links{list_link}')


def check_profiles(profiles, ALL_USER_INFORMATIONS):
    app_log("check_profiles", 'checking profiles to find new post')

    # steps:
    # search profiles that was read from db and then compare with data that in init db

    dtfr = read_information(ALL_USER_INFORMATIONS)
    for profile in profiles:

        go_to_profile(profile)

        csv_information = {}

        check_info = {}

        db_datetime = strToDatetime(
            dtfr.at[profile, 'last_post_date'] + ' ' + dtfr.at[profile, 'last_post_time'])

        time.sleep(PAGE_INTERACT_PERIOD)
        actual_username, followers, following, posts, last_post_date, last_post_time, likes, views, link_1, date_save, time_save, content_type = get_profile_and_last_post_information(
            profile)
        link = get_last_post_link()
        post_date, post_time, user, link, date_save, time_save = get_last_post_information(
            link)
        x = link_1[KEY_LINK]
        if x not in list_link:
            list_link.append(x)

        current_post_datetime = strToDatetime(post_date + ' ' + post_time)

        if db_datetime < current_post_datetime:
            # app_log("check_profiles", f'New post detected in {profile}. Adding "{profile}" to watchlist')
            app_log('check profiles',
                    f'New post detected in {profile}. Adding "{profile}" to watchlist')

            user_information = {KEY_USERNAME: profile}
            link = {KEY_LINK: link}
            date_save = {KEY_SAVE_DATE: date_save}

            csv_information.update(actual_username)
            csv_information.update(link_1)
            csv_information.update(likes)
            csv_information.update(views)
            csv_information.update(content_type)
            date, time_n = get_current_time_and_date()
            csv_information.update({'time': time_n})

            check_info.update(user_information)
            check_info.update(link_1)
            check_info.update(date_save)

            app_log('check_profiles', 'adding "{profile}" to task_manager')
            task_manager_update(TASK_LIST_CSV, check_info)
            # data_base updating
            app_log('check_profiles', 'updating "{profile}" to database...')

            replace_db(profile, ALL_USER_INFORMATIONS)
            add_new_row(csv_information, NEW)
        else:
            app_log('check_profiles', 'nothing detected')


def monitoring(profiles, ALL_USER_INFORMATIONS):
    app_log('monitoring', 'Monitoring Started!')
    check_profiles(profiles, ALL_USER_INFORMATIONS)


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


def replace_db(profile, ALL_USER_INFORMATIONS):
    dtfr = read_information(ALL_USER_INFORMATIONS)
    dicts = {}
    replace_dic = {}
    actual_username, followers, following, posts, last_post_date, last_post_time, likes, views, link, date_save, time_save, content_type = get_profile_and_last_post_information(
        profile)

    keys = [KEY_FOLLOWERS, KEY_FOLLOWING, KEY_POSTS, KEY_CONTENT, KEY_LIKES, KEY_VIEWS,
            KEY_LINK, KEY_LAST_POST_DATE, KEY_LAST_POST_TIME, KEY_SAVE_DATE, KEY_SAVE_TIME]

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
    df2 = dtfr.at[profile, 'followers'], dtfr.at[profile, 'following'], dtfr.at[profile, 'posts'], dtfr.at[profile, 'content_type'], dtfr.at[profile, 'likes'], dtfr.at[profile,
                                                                                                                                                                        'views'], dtfr.at[profile, 'link'], dtfr.at[profile, 'last_post_date'], dtfr.at[profile, 'last_post_time'], dtfr.at[profile, 'save_date'], dtfr.at[profile, 'save_time']
    for i, j in zip(keys, df2):
        dicts[i] = j

    df3 = dtfr.replace({dicts['followers']: replace_dic[KEY_FOLLOWERS], dicts['following']: replace_dic[KEY_FOLLOWING], dicts['posts']: replace_dic[KEY_POSTS], dicts['content_type']: replace_dic[KEY_CONTENT], dicts['likes']: replace_dic[KEY_LIKES], dicts['views']: replace_dic[KEY_VIEWS], dicts['link']: replace_dic[KEY_LINK], dicts['last_post_date']: replace_dic[KEY_LAST_POST_DATE], dicts['last_post_time']: replace_dic[KEY_LAST_POST_TIME], dicts['save_date']: replace_dic[KEY_SAVE_DATE], dicts['save_time']: replace_dic[KEY_SAVE_TIME]})
    print(df3)
    df3.to_csv(ALL_USER_INFORMATIONS)


def read_task_manager(file_path):
    task_list = []
    with open(file_path, 'r') as file:
        x = csv.reader(file)
        next(x)
        for i in x:
            task_dict = dict()
            task_dict['username'] = i[0]
            task_dict['link'] = i[1]

            task_list.append(task_dict)

    return task_list


# TODO: ADD METHODS IN THE (IF) FOR REMOVE LINK FROM ANY CSV!
def check_time(task_path, task_list):
    '''this def , find save_date any profile then calculate time for task_manager and each user_csv, after calculate must remove link from task_manager and stop calculation of user_csv'''
    app_log('check_time', 'here we are ')
    task_list = read_task_manager(task_path)
    date_now = datetime.datetime.now().date()

    for task in task_list:
        link = task['link']
        read_csv = pd.read_csv(task_path, index_col='link')
        find_pos = read_csv.at[task['link'], 'save_date']
        save_date = strToDatetime_csv(find_pos)
        remaining_days = (date_now - save_date).days
        if remaining_days >= 14:
            task_manager_expire(task_path, link)
            list_link.remove(link)
            app_log('check_time', 'remove link from task manager')
        else:
            app_log('check_time', f"continue checking = {link}")


# Main ________________________________________________
# we will sign into instagram and make environment ready to run script
def run_bot(users):
    """ this method will initialize bot """
    app_log("run_bot", "Let the show begin!")
    
    # init_instagram()
    login()
    
    
    initial_profile_database(users)
    # if not INIT_DATABASE_STATUS:
    #     initial_profile_database(profiles)


    # init a database of users information
    # keep eyes on profiles that post new content
    while True:
        try:
            monitoring(users, ALL_USER_INFORMATIONS)
            check_time(TASK_LIST_CSV, read_task_manager(TASK_LIST_CSV))
            time.sleep(WATCHLIST_PERIOD)
            update_info(list_link)
        except:
            with open(LIST_OF_LINKS, 'w') as f:
                for element in list(set(list_link)):
                    f.write(element + "\n")
# ---------------finish---------------------------------------------------------------

    # # if __name__ == '__main__':
    
    # if __name__ == '__main__':
    #     a = Thread(target = monitoring,args=[profiles, ALL_USER_INFORMATIONS])
    #     b = Thread(target = update_info,args=[list_link])
    #     a.start()
    #     b.start()
    #     finish = time.perf_counter()
    # print(f'finish running after seconds : {finish}')
            

       
# TODO: WARNING - edit here in production
if not DEBUG:
    profiles = get_usernames(PROFILES_USERNAME_DB)
else:
    profiles = get_usernames(PROFILES_USERNAME_DB)[:2]

run_bot(profiles)
