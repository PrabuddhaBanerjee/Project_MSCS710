from typing import List
import pymongo
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_basicAuth(username, password, required_scopes):
    client = pymongo.MongoClient('mongodb+srv://christiansumano:csumano1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client["airservices"]
    users = db["users"]
    
    if users.count_documents({"username":username, "password":password}) >= 1:
        return {'test_key': 'test_value'}


