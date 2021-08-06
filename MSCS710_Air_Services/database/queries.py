from pymongo import MongoClient
import pandas as pd
import json
import numpy as np
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from math import pi
from bokeh.palettes import Category10
from bokeh.transform import cumsum
from bokeh.palettes import Category20c


'''
Query all of one type of weather info
'''
def query_weather_data(info):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    weather = db["weather"]

    df = pd.DataFrame(list(weather.find({"info":info})))

    return(df)


'''
Query to pull out weather data from the database and return a pandas df
'''
def select_weather(city, info):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    weather = db["weather"]
    
    df = pd.DataFrame(list(weather.find({"city": city, "info":info})))
    if df.empty:
        return df
    df = df.drop(columns=["_id"])

    return df


'''
Query to pull airline data out for a specific date
'''
def select_airline_by_date(day, month, year):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flights = db["flights"]
    
    df = pd.DataFrame(list(flights.find({"DAY_OF_MONTH":str(day), "MONTH":str(month), "YEAR":str(year)})))
    if df.empty:
        return df
    df = df.drop(columns=["_id"])

    return df


'''
Query to pull airline data out for a specific date / city 
'''
def select_airline_by_date_and_city(day, month, year, city):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flights = db["flights"]

    df = pd.DataFrame(list(flights.find({"DAY_OF_MONTH":str(day), "MONTH":str(month), "YEAR":str(year), "ORIGIN_CITY_NAME":city})))
    if df.empty:
        return df
    df = df.drop(columns=["_id"])

    return df


def select_airline_by_date_and_origin(day, month, year,origin):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flights = db["flights"]

    df = pd.DataFrame(list(flights.find({"DAY_OF_MONTH":str(day), "MONTH":str(month), "YEAR":str(year),"ORIGIN_CITY_NAME":(origin)})))
    if df.empty:
        return df
    df = df.drop(columns=["_id"])

    return df


def select_airline_by_date_and_origin_woyear(day, month, origin):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flights = db["flights"]

    df = pd.DataFrame(list(flights.find({"DAY_OF_MONTH":str(day), "MONTH":str(month), "ORIGIN":(origin)})))
    if df.empty:
        return df
    df = df.drop(columns=["_id"])

    return df



def select_airline_by_date_and_origin_and_dest(day, month, year, origin,destination):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flights = db["flights"]

    df = pd.DataFrame(list(flights.find({"DAY_OF_MONTH":str(day), "MONTH":str(month), "YEAR":str(year), "ORIGIN_CITY_NAME":(origin),"DEST_CITY_NAME":(destination)})))
    if df.empty:
        return df
    df = df.drop(columns=["_id"])

    return df

def select_airline_by_date_and_dest(day, month, year,destination):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flight = db["flight"]

    df = pd.DataFrame(list(flight.find({"DAY_OF_MONTH":str(day), "MONTH":str(month), "YEAR":str(year),"DEST_CITY_NAME":(destination)})))
    if df.empty:
        return df
    df = df.drop(columns=["_id"])

    return df

def year_cancellations(year):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flights = db["flights"]
    
    jan = 0
    feb = 0 
    march = 0
    april = 0
    may = 0
    june = 0
    july = 0
    aug = 0
    sept = 0
    octo = 0
    nov = 0 
    dec = 0
    
    if year != None:
        for flight in flights.find({"CANCELLED":"1","YEAR":year}):
            print(flight)
            if flight['MONTH'] == "1":
                jan += 1
            if flight['MONTH'] == "2":
                feb += 1
            if flight['MONTH'] == "3":
                march += 1
            if flight['MONTH'] == "4" :
                april += 1
            if flight['MONTH'] == "5":
                may += 1
            if flight['MONTH'] == "6" :
                june += 1
            if  flight['MONTH'] == "7" :
                july += 1
            if flight['MONTH'] == "8" :
                aug+= 1
            if flight['MONTH'] == "9":
                sept += 1
            if flight['MONTH'] == "10":
                octo += 1
            if flight['MONTH'] == "11":
                nov += 1
            if flight['MONTH'] == "12":
                dec += 1
    else:
        for flight in flights.find({"CANCELLED":"1"}):
            print(flight)
            if flight['MONTH'] == "1":
                jan += 1
            if flight['MONTH'] == "2":
                feb += 1
            if flight['MONTH'] == "3":
                march += 1
            if flight['MONTH'] == "4" :
                april += 1
            if flight['MONTH'] == "5":
                may += 1
            if flight['MONTH'] == "6" :
                june += 1
            if  flight['MONTH'] == "7" :
                july += 1
            if flight['MONTH'] == "8" :
                aug+= 1
            if flight['MONTH'] == "9":
                sept += 1
            if flight['MONTH'] == "10":
                octo += 1
            if flight['MONTH'] == "11":
                nov += 1
            if flight['MONTH'] == "12":
                dec += 1

    months = ['jan', 'feb', 'march', 'april', 'may', 'june','july','aug','sept','octo','nov','dec']
    cancellations = [jan, feb, march, april, may, june,july,aug,sept,octo,nov,dec]

    p = figure(x_range=months, plot_height=250, title="Cancellations",
            toolbar_location=None)

    p.vbar(x=months, top=cancellations, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    html = file_html(p, CDN, "my plot")

    return html

def cancellation_reason():
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flight = db["flights"]

    carrier = flight.count_documents({"CANCELLATION_CODE":"0"})
    weather = flight.count_documents({"CANCELLATION_CODE":"1"})
    nas = flight.count_documents({"CANCELLATION_CODE":"2"})
    sec = flight.count_documents({"CANCELLATION_CODE":"3"})

    x = {
        "Carrier": carrier,
        "Weather": weather,
        "NAS": nas,
        "Security":sec
    }
   
    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'type'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(x)]
    #data['angle'][3] = 0.02

    p = figure(plot_height=350, title="Cancellation Reasons", toolbar_location="right",
            tools="hover,pan,wheel_zoom,box_zoom,reset", tooltips="@type: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='type', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None

    html = file_html(p, CDN, "my plot")

    return html


def weather_cancellations(year):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]

    weather = db['weather_canc']
    count = 0
    lis = weather.distinct("value")

    dic = {}
    weath_can = []
    canc = []

    if year != None:
        for i in lis:
            if weather.count_documents({"value":i, "year":year}) > 85:
                weath_can.append(weather.count_documents({"value":i}))
                canc.append(i)
                dic[i] = weather.count_documents({"value":i})

    else:
        for i in lis:
            if weather.count_documents({"value":i}) > 85:
                weath_can.append(weather.count_documents({"value":i}))
                canc.append(i)
                dic[i] = weather.count_documents({"value":i})

    dic.pop('sky is clear')
    data = pd.Series(dic).reset_index(name='value').rename(columns={'index':'Weather'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(dic)]

    p = figure(plot_height=350, title="Weather cancellation", toolbar_location="right",
            tools="hover,pan,wheel_zoom,box_zoom,reset", tooltips="@Weather: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='Weather', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None


    html = file_html(p, CDN, "my plot")

    return html


'''
Get a random records to use as supervisor for decision tree. Does not garuntee no dups
'''
def random_record(size):
    client = MongoClient('mongodb+srv://johnathonhoste:jhoste1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    flights = db["flights"]

    pipeline = [
        { "$sample": { "size": size } }
    ]

    df = pd.DataFrame(list(flights.aggregate(pipeline)))
    print(df)
    if df.empty:
        return df
    df = df.drop(columns=["_id"])

    return df
