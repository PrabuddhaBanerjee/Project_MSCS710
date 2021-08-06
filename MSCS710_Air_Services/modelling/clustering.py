import pandas as pd
import numpy as np
import math
from database import queries

#sklearn imports
from sklearn.decomposition import PCA #Principal Component Analysis
from sklearn.cluster import KMeans #K-Means Clustering
from sklearn.preprocessing import StandardScaler #used for 'Feature Scaling'

global cluster_model
global cluster_training_df

'''
Join queried weather data with airline records
'''
def join_weather_data(airline_df, in_weather_df, info):
    weather_df = in_weather_df[["value","year","month","day","hour"]]
    weather_df = weather_df.rename(columns={"year":"YEAR","month":"MONTH","day":"DAY_OF_MONTH","hour":"HOUR","value":info })
    joined_df = airline_df.merge(weather_df, on=['YEAR','MONTH','DAY_OF_MONTH','HOUR'])

    return joined_df


'''
Build a clustering model
'''
def cluster():
    print("Starting to create cluster model")
    starting_record_count = 50000 # Need enough records to make a non harming fit
    cluster_count = 8

    hum = queries.query_weather_data("humidity")
    pre = queries.query_weather_data("pressure")
    tem = queries.query_weather_data("temperature")
    wind_d = queries.query_weather_data("wind_direction")
    wind_s = queries.query_weather_data("wind_speed")

    df = queries.random_record(starting_record_count)
    df = join_weather_data(df, hum, "HUMIDITY")
    df = join_weather_data(df, pre, "PRESSURE")
    df = join_weather_data(df, tem, "TEMPERATURE")
    df = join_weather_data(df, wind_d, "WIND_DIRECTION")
    df = join_weather_data(df, wind_s, "WIND_SPEED")


    df.dropna(inplace=True)
    df = df.reset_index()

    # not using DEST / ORIGIN as it classifies badly
    dtdf = df[["MONTH","DAY_OF_WEEK","HOUR",
                "HUMIDITY","PRESSURE","TEMPERATURE","WIND_DIRECTION","WIND_SPEED"]]

    #Initialize our scaler
    scaler = StandardScaler()

    #Scale each column in numer
    dtdf = pd.DataFrame(scaler.fit_transform(dtdf))
    dtdf.columns=["MONTH","DAY_OF_WEEK","HOUR",
                    "HUMIDITY","PRESSURE","TEMPERATURE","WIND_DIRECTION","WIND_SPEED"]

    fitdf = dtdf.sample(dtdf.index.size)

    kmeans = KMeans(n_clusters=cluster_count, n_init=30)
    kmeans.fit(fitdf)

    return kmeans, df


'''
Classify records using the clustering model
Accepts a df of records as input to classify 
'''
def classify(cluster_model, cluster_df, df_sample):
    cluster_count = 8

    hum = queries.query_weather_data("humidity")
    pre = queries.query_weather_data("pressure")
    tem = queries.query_weather_data("temperature")
    wind_d = queries.query_weather_data("wind_direction")
    wind_s = queries.query_weather_data("wind_speed")
    wea = queries.query_weather_data("weather_description")

    df_sample = join_weather_data(df_sample, hum, "HUMIDITY")
    df_sample = join_weather_data(df_sample, pre, "PRESSURE")
    df_sample = join_weather_data(df_sample, tem, "TEMPERATURE")
    df_sample = join_weather_data(df_sample, wind_d, "WIND_DIRECTION")
    df_sample = join_weather_data(df_sample, wind_s, "WIND_SPEED")
    df_sample = join_weather_data(df_sample, wea, "WEATHER_DESC")

    df_sample.dropna(inplace=True)
    df_sample = df_sample.reset_index()
    concat_df = pd.concat([cluster_df, df_sample], axis=0, sort=False, ignore_index=True)
    concat_df_sub = concat_df[["MONTH","DAY_OF_WEEK","HOUR",
                    "HUMIDITY","PRESSURE","TEMPERATURE","WIND_DIRECTION","WIND_SPEED"]].copy()


    # Initialize a scaler 
    scaler = StandardScaler()
    scaled_df = pd.DataFrame(scaler.fit_transform(concat_df_sub))
    scaled_df.columns=["MONTH","DAY_OF_WEEK","HOUR",
                    "HUMIDITY","PRESSURE","TEMPERATURE","WIND_DIRECTION","WIND_SPEED"]
    
    concat_df.MONTH = scaled_df.MONTH
    concat_df.DAY_OF_WEEK = scaled_df.DAY_OF_WEEK
    concat_df.HOUR = scaled_df.HOUR
    concat_df.HUMIDITY = scaled_df.HUMIDITY
    concat_df.PRESSURE = scaled_df.PRESSURE
    concat_df.TEMPERATURE = scaled_df.TEMPERATURE
    concat_df.WIND_DIRECTION = scaled_df.WIND_DIRECTION
    concat_df.WIND_SPEED = scaled_df.WIND_SPEED

    cluster_df = concat_df.head(cluster_df.index.size).copy()
    df_sample = concat_df.tail(df_sample.index.size).copy()

    clusters = cluster_model.predict(scaled_df.head(cluster_df.index.size))
    cluster_df["Cluster"] = clusters
    clusters = cluster_model.predict(scaled_df.tail(df_sample.index.size))
    df_sample["Cluster"] = clusters
    
    cluster_cancel_rates = {}
    cluster_delay_rates = {}
    for i in range(0, cluster_count):
        cluster = cluster_df[cluster_df['Cluster'] == i].copy()
        cluster.loc[:,'DEP_DELAY_NEW'] = cluster['DEP_DELAY_NEW'].astype(int)
        if "1" in cluster['CANCELLED'].value_counts().index:
            cluster_cancel_rates[i] = cluster['CANCELLED'].value_counts()["1"]/(cluster.index.size)
        else:
            cluster_cancel_rates[i] = 0

        cluster_delay_rates[i] = cluster[cluster['DEP_DELAY_NEW'] > 0].index.size/(cluster.index.size)

    canc_rate = 0
    delay_rate = 0
    for cluster in df_sample['Cluster'].value_counts().index.tolist():
        canc_rate += (df_sample['Cluster'].value_counts()[cluster]/df_sample['Cluster'].value_counts().index.size) * cluster_cancel_rates[cluster]
        delay_rate += (df_sample['Cluster'].value_counts()[cluster]/df_sample['Cluster'].value_counts().index.size) * cluster_delay_rates[cluster]

    # return an average of classification percentages
    return canc_rate, delay_rate
    
