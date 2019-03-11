import sys
import os
up_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
sys.path.append(up_dir)
from config import Config
from pymongo import MongoClient



config = Config()
mongo_obj = config.get('mongodb')
client = MongoClient(mongo_obj['host'], mongo_obj['port'])
db = client[mongo_obj['db']]
api_key_collection = db[mongo_obj['api_key_collection']]

expiration_in_seconds = config.get('seconds_till_expiration')
api_key_collection.create_index("createdAt", expireAfterSeconds=expiration_in_seconds)