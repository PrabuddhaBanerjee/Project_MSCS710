from pymongo import MongoClient

import pandas as pd
import glob
import numpy as np
import csv
import json

client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
db = client["airservices"]

weath = db['weather_description']

df = pd.read_csv("../weather_data/weather_description.csv")

headers = df.columns.tolist()

dates = df.iloc[:, 0]
count = 0 
print(len(df))

for i in range(0, len(df)):

    for j in range(1, len(headers)):     
        year = dates[i][0:4]
        month = dates[i][5:7].lstrip("0")
        day = dates[i][8:10].lstrip("0")
        hour = dates[i][11:13].lstrip("0")
        if hour == "":
            hour = 0
        row = {
            'city': headers[j],
            'value': df.at[i,headers[j]],
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
        }
        if hour == '12':
            count = count + 1
            print(count,row)
            weath.insert_one(row)
        else:
            continue