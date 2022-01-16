import os
import pandas as pd


CSV_FILE = os.path.dirname(__file__)
def make_csv_for_urls(pros):
    for pro in pros:
        path = CSV_FILE  +'\\' + pro 
        csv_path = path + '\\' + pro + '.csv'
        df = pd.read_csv(csv_path)
        print(df)

make_csv_for_urls("pros")