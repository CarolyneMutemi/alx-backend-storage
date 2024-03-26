#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB.
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    nginx = db.nginx

    print(f"{nginx.count_documents({})} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        result = nginx.count_documents({"method": method})
        print(f"\tmethod {method}: {result}")

    status_check = nginx.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")
