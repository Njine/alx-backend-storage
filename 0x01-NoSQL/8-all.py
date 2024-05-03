#!/usr/bin/env python3
"""
A Python function that retrieves all documents from a MongoDB collection.
Returns an empty list if no documents are found.
"""

def list_all(mongo_collection):
    """
    Lists all documents in the specified MongoDB collection.
    
    Parameters:
    - mongo_collection: The pymongo collection object to query.

    Returns:
    - A list of all documents in the collection, or an empty list if there are none.
    """
    return list(mongo_collection.find())
