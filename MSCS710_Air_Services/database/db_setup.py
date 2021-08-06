from pymongo import MongoClient
import pandas as pd
import glob
import numpy as np
import csv


def correct_encoding(dictionary):
    """Correct the encoding of python dictionaries so they can be encoded to mongodb
    inputs
    -------
    dictionary : dictionary instance to add as document
    output
    -------
    new : new dictionary with corrected encodings"""

    new = {}
    for key1, val1 in dictionary.items():
        # Nested dictionaries
        if isinstance(val1, dict):
            val1 = correct_encoding(val1)

        if isinstance(val1, np.bool_):
            val1 = bool(val1)

        if isinstance(val1, np.int64):
            val1 = int(val1)

        if isinstance(val1, np.float64):
            val1 = float(val1)

        new[key1] = val1

    return new


# Connect to the database
#client = MongoClient('mongodb+srv://daynaeidle:deidle1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority')
#db = client.airservices
client = MongoClient("mongodb://localhost:27017/")
db = client["airservices"]

print("Database created")

# Create collections
'''
db.flights.drop()
db.weather.drop()
db.users.drop()

flights = db.flights
weather = db.weather
users = db.users'''

flights = db["flights"]
weather = db["weather"]
users = db["users"]

print("Collections created")

# Get all flight files
flight_path = r'airline_data'
flight_filenames = glob.glob(flight_path + "/*.csv")

# Get all weather files
weather_path = r'..weather_data'
weather_filenames = glob.glob(weather_path + "/*.csv")


# Loop through flight files and add data to database
for file in flight_filenames:
    if file == "airline_data/airlines_final.csv":
        print(file)
    
        df = csv.DictReader(open(file))
        #flights.insert_many(df)
        #flight_file = file.rsplit('/', 1)[1]
        #flight_file = flight_file.split('.')[0]

        df = pd.read_csv(file)

        '''
        print(df.dtypes)
        for col in df.columns:
            df[col] = df[col].astype(object)
        print(df.dtypes)
        '''

        headers = df.columns.tolist()

        for i in range(len(df)):
            print(i)
            row = {}
            for j in range(len(headers)):
                row[headers[j]] = df.iloc[i, j]
            #row = correct_encoding(row)
            flights.insert_one(row)


# Loop through weather files and add data to database
for file in weather_filenames:
    print(file)
    weather_file = file.rsplit('/', 1)[1]
    weather_file = weather_file.split('.')[0]

    df = pd.read_csv(file)
    # df = df.head()
    headers = df.columns.tolist()

    dates = df.iloc[:, 0]

    for i in range(0, len(df)):
        for j in range(1, len(headers)):
            year = dates[i][0:4]
            month = dates[i][5:7].lstrip("0")
            day = dates[i][8:10].lstrip("0")
            hour = dates[i][11:13].lstrip("0")
            if hour == "":
                hour = 0
            row = {'city': headers[j],
                    'info': weather_file,
                    'value': df.at[i,headers[j]],
                    'year': year,
                    'month': month,
                    'day': day,
                    'hour': hour,
                    }
        #print(row)
            weather.insert_one(row)
            break
