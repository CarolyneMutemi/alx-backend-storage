#!/usr/bin/env python3
"""
Log stats - new version.
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

    ip_query = [
        {"$group": {"_id": "$ip", "count": {"$count": {}}}},
        {"$sort": {"count": -1, "_id": -1}},
        {"$limit": 10}
    ]

    print("IPs:")
    result_stats = nginx.aggregate(ip_query)
    for stat in result_stats:
        print(f'\t{stat.get("_id")}: {stat.get("count")}')
