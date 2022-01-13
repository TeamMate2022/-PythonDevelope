#This function convert csv file to chart


# Install matplotlib.pyplot and pands library
import matplotlib.pyplot as plt
import pandas as pd
from pandas.tseries.offsets import YearEnd
import numpy as np
import math

#Make function for 6 Parameter

def draw_csv(file_path , param_x , param_y, param_z, param_d, param_f):

    X = np.arange(0, math.pi*2, 0.05)
    figure, axis = plt.subplots(2, 2)
    
# plt.style.use For make appearance title 
    #plt.style.use('bmh')

#Read CSV File (Should Code and CSV-file on Folder)
    df = pd.read_csv(file_path)

# Naming for parameters
    x = df[param_x]
    y = df[param_y]
    z = df[param_z]
    d = df[param_d]
    f = df[param_f]


# Multi Chart
    axis[0, 0].plot(x,y)
    axis[0, 0].set_title("SaveTime - Like")

    axis[0, 1].plot(x,z)
    axis[0, 1].set_title("SaveTime - Posts")

    axis[1, 0].plot(x,d)
    axis[1, 0].set_title("SaveTime - Followers")

    axis[1, 1].plot(x,f)
    axis[1, 1].set_title("SaveTime - Following")
# Show Chart
    plt.show()

draw_csv('sample.csv', 'save_time' , 'likes' , 'posts' , 'followers' , 'following')