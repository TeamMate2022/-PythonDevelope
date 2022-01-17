

import os
import csv
import shutil
import datetime
WRITE = 'w'

CSV_FILE = os.path.dirname(__file__)
def make_csv_file (pros):
    try:

        path = CSV_FILE  + '\\' + pros['username']
        os.mkdir(path)
        path + '\\' + pros['username'] + '.csv'
    except FileExistsError:
        # path = CSV_FILE  + '\\' + pros['username']
        # # shutil.rmtree(path)
        # os.mkdir(path)
        # path + '\\' + pros['username'] + '.csv'
        pass
        
    # with open(csv_path,'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["url"])



WRITE = 'w'
APPEND = 'a'

def add_new_row(pros, action):

        path = CSV_FILE  +'\\' + pros['username']
        
        csv_path = path + '\\' + pros['username'] + '.csv'
        url_path = path + '\\' + pros['url'] + '.csv'

        new_row = pros['url']

        print(type(new_row))
        # os.mkdir(url_path)
        # print(url_path)

        headers = ['url']

        print(headers)
        
        header = list(pros.keys())

        if action == WRITE:
            with open(csv_path, 'w', newline= '') as csv_file:
                
                writer = csv.DictWriter(csv_file,fieldnames = headers)
                
                writer.writeheader()

                writer.writerow({'url': pros['url']})

            with open (url_path , "w" , newline = "") as file:
                writer = csv.DictWriter(file,fieldnames = header)
                writer.writeheader()
                writer.writerow(pros)
                
        if action == APPEND:
            with open(csv_path, 'a', newline= '') as csv_file:
                
                writer = csv.DictWriter(csv_file,fieldnames = headers)
                
                # writer.writeheader()

                writer.writerow({'url': pros['url']})

            with open (url_path , "a" , newline = "") as file:
                header = list(pros.keys())
                print(header)
                writer = csv.DictWriter(file,fieldnames = header)
                # writer.writeheader()
                writer.writerow(pros)
         

info = {'username' : 'amir',
        "url" : 'hawwwfwqefef' ,
        "type" : 'image',
        "likes" : 42323,
        "views" : 2534237643676,
        "time" :  datetime.datetime.now().now().strftime("%X")}



make_csv_file(info)
add_new_row(info,APPEND)











# elif action == APPEND:
    # with open(csv_path, 'a', newline= '') as csv_file:
    #     writer = csv.DictWriter(csv_file,fieldnames = headers )
    #     writer.writerow(new_row)
# df = pd.read_csv(csv_path)
# df = df.append(new_row , ignore_index=True)
# print(df)