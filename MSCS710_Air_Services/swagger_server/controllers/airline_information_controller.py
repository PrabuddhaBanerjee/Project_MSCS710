import connexion
import six
import json

from swagger_server.models.airline_results import AirlineResults  # noqa: E501
from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.body1 import Body1  # noqa: E501
from swagger_server.models.body2 import Body2  # noqa: E501
from swagger_server import util

from database import queries
from modelling import reliability
from modelling import decision_tree
from modelling import clustering
from utilities import glb_handles


def best_airlines(body=None):  # noqa: E501
    """Best airports

    Get the best airports for a given date # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: AirlineResults
    """
    if connexion.request.is_json:
    
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
        data = queries.select_airline_by_date(body.day, body.month, body.year)
        rel_json = reliability.airline_reliability(data)
        return rel_json
        
    return 'Could not get flight data'


def flight_predictor(model, body=None):  # noqa: E501
    """Flight predictor

    Get predictions if a flight will be cancelled # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Body2.from_dict(connexion.request.get_json())  # noqa: E501
        data = queries.select_airline_by_date_and_origin_woyear(body.day, body.month, body.origin)
        if data.empty:
            return 'Could not get flight data'
        if model == "Supervised":
            canc_result = decision_tree.classify(glb_handles.canc_root_node, glb_handles.canc_dt, data, False)
            delay_result = decision_tree.classify(glb_handles.delay_root_node, glb_handles.delay_dt, data, True)
        elif model == "Unsupervised":
            canc_result, delay_result = clustering.classify(glb_handles.cluster_model, glb_handles.cluster_df, data) 
        elif model == "Ensembled":
            supervised_canc_result = decision_tree.classify(glb_handles.canc_root_node, glb_handles.canc_dt, data, False)
            supervised_delay_result = decision_tree.classify(glb_handles.delay_root_node, glb_handles.delay_dt, data, True)
            unsupervised_canc_result, unsupervised_delay_result = clustering.classify(glb_handles.cluster_model, glb_handles.cluster_df, data)
            canc_result = (supervised_canc_result + unsupervised_canc_result) / 2
            delay_result = (supervised_delay_result + unsupervised_delay_result) / 2

        return "Cancelation Chance: " + str(canc_result) + " , Delay Chance: " + str(delay_result)
        
    return 'Could not get flight data'


def weather_airline(body=None):  # noqa: E501
    """Weather comapred to flights

    Reports back weather type and cancellations beacause of that weather # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Body1.from_dict(connexion.request.get_json())  # noqa: E501
        data = queries.select_airline_by_date_and_city(body.day, body.month, body.year, body.city)
        rel_json = decision_tree.decision_tree(data)
        return rel_json
    return 'do some magic!'

def gather_flights(year, month=None, day=None, origin=None, destination=None):  # noqa: E501
    """Gather flight data

     # noqa: E501

    :param year: 
    :type year: int
    :param month: 
    :type month: int
    :param day: 
    :type day: int
    :param city: 
    :type city: str

    :rtype: None
    """
    if origin != None and destination != None:

        data = queries.select_airline_by_date_and_origin_and_dest(day, month, year, origin, destination)
        df = data.to_json()
        return df
    elif origin != None:
        data = queries.select_airline_by_date_and_origin(day, month, year, origin)
        df = data.to_json()
        return df
    elif destination != None:
        data = queries.select_airline_by_date_and_origin(day, month, year, destination)
        df = data.to_json()
        return df
    else:
        data = queries.select_airline_by_date(day, month, year)
        df = data.to_json()
        return df

    return 'Invalid'

def flight_graphs(graph, year=None):  # noqa: E501
    """Gather graphs
    Get a graph based on airport city and date # noqa: E501
    :param body: 
    :type body: dict | bytes
    :rtype: str
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
    
    if graph == "Cancellations":
        return queries.year_cancellations(year)
    
    if graph == "Weather":
        return queries.weather_cancellations(year)
