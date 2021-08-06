import connexion
import six
import pymongo

from swagger_server import util


def create_user(body=None):  # noqa: E501
    """Create user
    This can only be done by the logged in user. # noqa: E501
    :param body: 
    :type body: dict | bytes
    :rtype: None
    """
    # if connexion.request.is_json:
    #     body = Dict.from_dict(connexion.request.get_json())  # noqa: E501
    try:         
        client = pymongo.MongoClient('mongodb+srv://christiansumano:csumano1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
        db = client["airservices"]

        users = db["users"]
        username = body.get("username")
        email = body.get("email")
        password = body.get("password")
        
        if users.count_documents({"email":email}) == 0:
            if users.count_documents({"username":username}) == 0:
                users.insert_one(body)
            else:
                return 'Not registered username already exists. Please try again'
        else:
            return 'Not registered, email already registerd. Please try again'

        return 'Successfully registered'
    except:
        return 'Cannot connect to db'

def login_user(body=None):  # noqa: E501
    """Login user
    Register an account to use other features. # noqa: E501
    :param body: 
    :type body: dict | bytes
    :rtype: None
    """
    # if connexion.request.is_json:
    #     body = Dict.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        client = pymongo.MongoClient('mongodb+srv://christiansumano:csumano1@airservices.0mc0k.mongodb.net/AirServices?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE')
        db = client["airservices"]

        users = db["users"]
        password = body.get("password")
        email = body.get("email")

        print(users.count_documents({"email":email}))
        
        if users.count_documents({"email":email, "password":password}) == 1:
            return 'Success'
        else:
            return 'Invalid login, check email or password'
    except: 
        return 'could not connect to db'