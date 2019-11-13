import os 
from pymongo import MongoClient

host = os.environ['MONGO_HOST']
port = int(os.environ['MONGO_PORT'])

def (function):

    def wrapper(*args, **kwargs):

        # open connection 
        conn = MongoClient(host=host, port=port)

        function(*args, **kwargs, conn=conn)

        conn.close()

    return wrapper
