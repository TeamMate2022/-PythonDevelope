#This function convert csv file to chart

# Install matplotlib.pyplot and pands library
import requests
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import pylab
from pandas.tseries.offsets import YearEnd
import numpy as np
import math

#Make function for 5 Parameter
def draw_csv(param_x , param_y, param_z, param_d, param_f):

# Create Figure chart and custome (figsize for Resolution)
    X = np.arange(0, math.pi*2, 0.05)
    figure, axis = plt.subplots(2, 2 , figsize=(19.20,10.80))
#Change Figure Title Name
    figure.title_name('InstaScraper')
# plt.style.use For make appearance title

#Open CSV from "YourDocuments" 
    df = pd.read_csv (r"C:\Users\<YourDocuments>\Pictures\sample.csv")
    
# Naming for parameters
    x = df[param_x]
    y = df[param_y]
    z = df[param_z]
    d = df[param_d]
    f = df[param_f]
    
# Multi Chart
    axis[0, 0].plot(x,y)
    axis[0, 0].set_title("SaveTime : Like")
    axis[0, 1].stem(x,z)
    axis[0, 1].set_title("SaveTime : Posts")
    axis[1, 0].bar(x,d)
    axis[1, 0].set_title("SaveTime : Followers")
    axis[1, 1].step(x,f)
    axis[1, 1].set_title("SaveTime : Following")
# Save PNG from "YourDocuments" Hussain
    plt.savefig(r"C:\Users\<YourDocuments>\Pictures\test.png")
    plt.show()

draw_csv('save_time' , 'likes' , 'posts' , 'followers' , 'following')