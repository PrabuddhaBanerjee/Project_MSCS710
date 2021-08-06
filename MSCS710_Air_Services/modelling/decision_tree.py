import pandas as pd
from database import queries as qrs
import DecisionTree

'''
Join queried weather data with airline records
'''
def join_weather_data(airline_df, in_weather_df, info):
    weather_df = in_weather_df[["value","year","month","day","hour"]]
    weather_df = weather_df.rename(columns={"year":"YEAR","month":"MONTH","day":"DAY_OF_MONTH","hour":"HOUR","value":info })
    joined_df = airline_df.merge(weather_df, on=['YEAR','MONTH','DAY_OF_MONTH','HOUR'])

    return joined_df


'''
Decision tree model to predict boolean delay and boolean cancellation
'''
def create_decision_tree():
    starting_record_count = 100 # Need enough records to make a non harming fit
    leaf_threshold = 0.001

    # I don't consider all columns to be features because some are not directly correlated with CANCELLED
    feature_tree = [] # decision tree

    hum = qrs.query_weather_data("humidity")
    pre = qrs.query_weather_data("pressure")
    tem = qrs.query_weather_data("temperature")
    wind_d = qrs.query_weather_data("wind_direction")
    wind_s = qrs.query_weather_data("wind_speed")
    wea = qrs.query_weather_data("weather_description")

    # get a set of random airline records
    dtdf = qrs.random_record(starting_record_count)

    dtdf = join_weather_data(dtdf, hum, "HUMIDITY")
    dtdf = join_weather_data(dtdf, pre, "PRESSURE")
    dtdf = join_weather_data(dtdf, tem, "TEMPERATURE")
    dtdf = join_weather_data(dtdf, wind_d, "WIND_DIRECTION")
    dtdf = join_weather_data(dtdf, wind_s, "WIND_SPEED")
    dtdf = join_weather_data(dtdf, wea, "WEATHER_DESC")

    canc_df = dtdf[["MONTH","DAY_OF_WEEK","HOUR","CANCELLED",
                    "HUMIDITY","PRESSURE","TEMPERATURE","WIND_DIRECTION","WIND_SPEED","WEATHER_DESC"]].copy()
    delay_df = dtdf[["MONTH","DAY_OF_WEEK","HOUR","DEP_DELAY_GROUP",
                    "HUMIDITY","PRESSURE","TEMPERATURE","WIND_DIRECTION","WIND_SPEED","WEATHER_DESC"]].copy()
    delay_df.loc[:,"DELAYED"] = ["0" if int(x) < 1 else "1" for x in dtdf.DEP_DELAY_GROUP]


    # drops rows with incomplete information
    canc_df = canc_df.dropna().copy()
    delay_df = delay_df.dropna().copy()

    # adjust to the new amount of records
    canc_record_count = canc_df.index.size
    delay_recoud_count = delay_df.index.size

    # decision tree module needs to read fro ma csv file
    canc_df.to_csv("canc_dt_training.csv")
    delay_df.to_csv("delay_dt_training.csv")

    # Create the decision trees
    canc_dt = DecisionTree.DecisionTree(
        training_datafile = "canc_dt_training.csv",
        csv_class_column_index = 4,
        csv_columns_for_features = [1,2,3,5,6,7,8,9,10],
        entropy_threshold = leaf_threshold,
        max_depth_desired = 9,
        symbolic_to_numeric_cardinality_threshold = 25,
    )

    canc_dt.get_training_data()
    canc_dt.calculate_first_order_probabilities()
    canc_dt.calculate_class_priors()
    #canc_dt.show_training_data()
    canc_root_node = canc_dt.construct_decision_tree_classifier()


    delay_dt = DecisionTree.DecisionTree(
        training_datafile = "delay_dt_training.csv",
        csv_class_column_index = 11,
        csv_columns_for_features = [1,2,3,5,6,7,8,9,10],
        entropy_threshold = leaf_threshold,
        max_depth_desired = 9,
        symbolic_to_numeric_cardinality_threshold = 25,
    )

    delay_dt.get_training_data()
    delay_dt.calculate_first_order_probabilities()
    delay_dt.calculate_class_priors()
    #delay_dt.show_training_data()
    delay_root_node = delay_dt.construct_decision_tree_classifier()


    return canc_root_node, canc_dt, delay_root_node, delay_dt
    

'''
Classify records using the decision tree model
Accepts a df of records as input to classify 
'''
def classify(root_node, dt, df_sample, canc_delay):

    hum = qrs.query_weather_data("humidity")
    pre = qrs.query_weather_data("pressure")
    tem = qrs.query_weather_data("temperature")
    wind_d = qrs.query_weather_data("wind_direction")
    wind_s = qrs.query_weather_data("wind_speed")
    wea = qrs.query_weather_data("weather_description")

    df_sample = join_weather_data(df_sample, hum, "HUMIDITY")
    df_sample = join_weather_data(df_sample, pre, "PRESSURE")
    df_sample = join_weather_data(df_sample, tem, "TEMPERATURE")
    df_sample = join_weather_data(df_sample, wind_d, "WIND_DIRECTION")
    df_sample = join_weather_data(df_sample, wind_s, "WIND_SPEED")
    df_sample = join_weather_data(df_sample, wea, "WEATHER_DESC")

    df_sample.dropna(inplace=True)

    if canc_delay == False:
        df_sample = df_sample[["MONTH","DAY_OF_WEEK","HOUR","ORIGIN","CANCELLED",
                            "HUMIDITY","PRESSURE","TEMPERATURE","WIND_DIRECTION","WIND_SPEED","WEATHER_DESC"]]

    elif canc_delay == True:
        df_sample.loc[:,"DELAYED"] = ["0" if int(x) < 1 else "1" for x in df_sample.DEP_DELAY_GROUP]
        df_sample = df_sample[["MONTH","DAY_OF_WEEK","HOUR","ORIGIN",
                            "HUMIDITY","PRESSURE","TEMPERATURE","WIND_DIRECTION","WIND_SPEED","WEATHER_DESC","DELAYED"]]



    class_list = []
    for i, row in df_sample.iterrows():
        test_sample = [
            "MONTH = " + row.MONTH,
            "DAY_OF_WEEK = " + row.DAY_OF_WEEK,
            "HOUR = " + row.HOUR,
            "HUMIDITY = " + str(row.HUMIDITY),
            "PRESSURE = " + str(row.PRESSURE),
            "TEMPERATURE = " + str(row.TEMPERATURE),
            "WIND_DIRECTION = " + str(row.WIND_DIRECTION),
            "WIND_SPEED = " + str(row.WIND_SPEED),
            "WEATHER_DESC = " + row.WEATHER_DESC
        ] 

        classification = dt.classify(root_node, test_sample)

        if canc_delay == False:
            class_list.append(classification["CANCELLED=0"])
        elif canc_delay == True:
            class_list.append(classification["DELAYED=0"])

    class_list_f = [float(i) for i in class_list]

    # return an average of classification percentages
    return 1 - (sum(class_list_f) / len(class_list_f))

