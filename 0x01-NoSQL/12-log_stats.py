#!/usr/bin/env python3
"""
Python script to provide statistics from Nginx logs stored in a MongoDB collection.
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    
    # Total number of logs in the collection
    log_count = logs_collection.count_documents({})
    print(f"{log_count} logs")
    
    # Print counts for each HTTP method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = logs_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count documents with GET method and /status path
    status_check_count = logs_collection.count_documents({
        "method": "GET",
        "path": "/status"
    })
    print(f"{status_check_count} status check")
