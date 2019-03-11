import sys
import os
from pymongo import MongoClient
sys.path.append(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..'))
from config import Config


class MongoHelper():
    def __init__(self):
        self.db = None
        self.api_key_collection = None
        self.client = None
        self.config = Config()
        self.mongo_config = self.config.get('mongodb')
        

    def mongo_connect(self):
        mongo_obj = self.mongo_config
        self.client = MongoClient(mongo_obj['host'], mongo_obj['port'])
        self.db = self.client[mongo_obj['db']]
        self.api_key_collection = self.db[mongo_obj['api_key_collection']]
    
