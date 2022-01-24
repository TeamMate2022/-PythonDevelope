
import math
import time , datetime
import pandas as pd
import csv


task = r"D:\TeamMates\python\insta-v1\InstaScraper\instascraper data\task_manager.csv"

def strToDatetime_csv(str_date_time):
    # this def read times in csv and change format with this model month/day/year to year/month/day
    try:
        datetime_format = "%Y-%M-%d"
        csv_time = datetime.datetime.strptime(str_date_time, datetime_format).date()
    except:
        datetime_format = "%m/%d/%Y"
        csv_time = datetime.datetime.strptime(str_date_time, datetime_format).date()
    
    # print(csv_time)
    return csv_time

#TODO: ADD METHODS IN THE (IF) FOR REMOVE LINK FROM ANY CSV!
def check_time(task_path):
    '''this def , find save_date any profile then calculate time for task_manager and each user_csv, after calculate must remove link from task_manager and stop calculation of user_csv'''
   
    task_list = []
    date_now = datetime.datetime.now().date()
    
    with open (task_path , 'r') as file:
        x = csv.reader(file)
        next(x)
        for i in x:
            
            task_dict = dict()
            task_dict['username'] = i[0]
            task_dict['link'] = i[1]
            
            task_list.append(task_dict)
    
    for task in task_list:
        link = task['link']
        read_csv = pd.read_csv(task_path , index_col = 'link')
        find_pos = read_csv.at[task['link'], 'save_date']
        save_date = strToDatetime_csv(find_pos)
        remaining_days = (date_now - save_date).days
        if remaining_days >= 14:
            print("remove link")
        else:
            print("continue checking")



check_time(task)


