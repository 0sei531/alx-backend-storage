#!/usr/bin/env python3
"""
Python script that provides stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    Retrieves and prints stats about Nginx logs from MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.
    """
    n_logs = mongo_collection.count_documents({})
    print(f'{n_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f'{status_check} status check')

if __name__ == "__main__":
    # MongoDB connection
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Retrieve and print stats
    log_stats(nginx_collection)
