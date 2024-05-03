#!/usr/bin/env python3
"""
Python function to insert a new document into a MongoDB collection using keyword arguments.
"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the specified MongoDB collection with data from **kwargs.

    Parameters:
    - mongo_collection: The pymongo collection object where the document will be inserted.
    - **kwargs: The data to be inserted into the new document.

    Returns:
    - The _id of the newly inserted document.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
