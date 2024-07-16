#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """
from pymongo import MongoClient

if __name__ == "__main__":
    """ Provides some stats about Nginx logs stored in MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    
    try:
        client.admin.command('ismaster')
        print("Connected successfully to MongoDB!")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        exit(1)

    nginx_collection = client.logs.nginx

    sample_doc = nginx_collection.find_one()
    if sample_doc:
        print("Sample document structure:")
        print(sample_doc)
    else:
        print("No documents found in the collection")

    n_logs = nginx_collection.count_documents({})
    print(f'{n_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f'{status_check} status check')

    pipeline = [
        {"$group": {"_id": "$remote_addr", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    print("Aggregation result:")
    for doc in nginx_collection.aggregate(pipeline):
        print(doc)

    print("IPs:")
    for doc in nginx_collection.aggregate(pipeline):
        ip = doc["_id"]
        count = doc["count"]
        print(f'\t{ip}: {count}')
