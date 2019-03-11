
import os
import sys

from flask import Flask, request, abort, jsonify
from functools import wraps

import uuid
from pymongo import MongoClient

from datetime import timedelta, datetime
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from config import Config


class ApiKeyManager():
    def __init__(self):
        self.config = Config()
        self.client = None
        self.db = None
        self.api_key_collection = None
        self.valid_keys = []
        self.set_api_key()

    def require_appkey(self, view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            if 'Authorization' in request.headers:
                raw_auth_key = request.headers['Authorization']
                auth_key = raw_auth_key.replace('Bearer ', '')
            else:
                error_message = 'Authorization key is required in header example: Bearer API_KEY'
                return jsonify(message=error_message), 403

            if auth_key and auth_key not in self.valid_keys:
                self.set_api_key()
            if auth_key and auth_key in self.valid_keys:
                return view_function(*args, **kwargs)
            else:
                error_message = "Unauthorized: Invalid or expired API key"
                return jsonify(message=error_message), 401
        return decorated_function

    def generate_key(self):
        key = uuid.uuid4().hex
        key = key.upper()[0:self.config.get('api_key_length')]
        return key

    def create_key(self, uuid, email, app_name):
        self.mongo_connect()
        key = self.generate_key()
        utc_now = datetime.utcnow()
        seconds_till_expire = self.config.get('seconds_till_expiration')
        expire_date = utc_now + timedelta(seconds=seconds_till_expire)
        api_key_doc = {
            "apiKey": key,
            "expiration_notice": {
                'notice1': False,
                'notice2': False,
                'final_notice': False
            },
            "uuid": uuid,
            'email': email,
            "application": app_name,
            "createdAt": utc_now,
            "expirationDate": expire_date
        }
        self.api_key_collection.insert_one(api_key_doc)
        self.client.close()
        return api_key_doc

    def set_api_key(self):
        self.mongo_connect()
        key_obj = self.api_key_collection.find({})
        self.valid_keys = [x['apiKey'] for x in key_obj]

    # TODO set collection from config

    def mongo_connect(self):
        mongo_obj = self.config.get('mongodb')
        self.client = MongoClient(mongo_obj['host'], mongo_obj['port'])
        self.db = self.client[mongo_obj['db']]
        self.api_key_collection = self.db[mongo_obj['api_key_collection']]
