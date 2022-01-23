
import math
import time , datetime
import pandas as pd


task = r"D:\TeamMates\python\insta-v2\InstaScraper\task_manager.csv"

def strToDatetime_csv(str_date_time):
    
    # this def read times in csv and change format with this model month/day/year to year/month/day
    
    datetime_format = "%Y-%M-%d"
    return datetime.datetime.strptime(str_date_time, datetime_format).date()

#TODO: ADD METHODS IN THE (IF) FOR REMOVE LINK FROM ANY CSV!
def check_time(task_path):
    
    # this def , find save_date any profile then calculate time for task_manager and each user_csv, after calculate must remove link from task_manager and stop calculation of user_csv
    date_now = datetime.datetime.now().date()
    
    for profile in profiles:
        df = pd.read_csv(task_path , index_col = 'username')
        df2 = df.at[profile , 'save_date']
        df2 = strToDatetime_csv(df2)
    
    result = str(abs(date_now - df2)).split(' ')
    
    time = int(result[0])
    
    if time >= 14:
        print("remove link")
    else:
        print("continue checking")



check_time(task)


