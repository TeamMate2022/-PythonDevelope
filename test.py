

import os
import pandas as pd
import csv

APPEND = 'a'
WRITE = 'w'

CSV_FILE = os.path.dirname(__file__)
def make_csv_file (pros):
    for pro in pros:
        path = CSV_FILE  +'\\' + pro 
        os.mkdir(path)
        path + '\\' + pro + '.csv'

        # with open(csv_path,'w') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(["url"])


make_csv_file("pros")

def add_new_row(pros,action):
    
        for pro in pros:
            path = CSV_FILE  +'\\' + pro 
            csv_path = path + '\\' + pro + '.csv'
            new_row = {'url':'1233444412123'}
            headers = list(new_row.keys())
             
            if action == WRITE:
                with open(csv_path, 'w', newline= '') as csv_file:   

                    writer = csv.DictWriter(csv_file,fieldnames = headers)
                    writer.writeheader()  
                    writer.writerow(new_row) 
                
            elif action == APPEND:
                with open(csv_path, 'a', newline= '') as csv_file:       
                    writer = csv.DictWriter(csv_file,fieldnames = headers )
                    writer.writerow(new_row)
            # df = pd.read_csv(csv_path)
            # df = df.append(new_row , ignore_index=True)
            # print(df)
add_new_row("pros", WRITE)