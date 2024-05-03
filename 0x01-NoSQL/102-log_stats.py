#!/usr/bin/env python3
"""
Improved Python script to provide Nginx log statistics from a MongoDB collection,
including a top 10 list of the most common IPs.
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    # Count total logs in the collection
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

    # Aggregate the top 10 most common IPs, sorted in descending order by count
    top_ips = logs_collection.aggregate([
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}  # Count occurrences of each IP
            }
        },
        {
            "$sort": {
                "count": -1  # Sort by count in descending order
            }
        },
        {
            "$limit": 10  # Limit to top 10 IPs
        }
    ])

    # Output the top 10 IPs with their respective counts
    print("IPs:")
    for doc in top_ips:
        print(f"\t{doc['_id']}: {doc['count']}")
