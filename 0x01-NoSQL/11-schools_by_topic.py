#!/usr/bin/env python3
"""
Python function that retrieves a list of schools that have a specific topic in their 'topics' field.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools that have a specific topic in their 'topics' field.
    
    Parameters:
    - mongo_collection: The pymongo collection object to query.
    - topic: A string representing the topic to search for.

    Returns:
    - A list of school documents that contain the specified topic in their 'topics' field.
    """
    return list(mongo_collection.find({"topics": {"$elemMatch": {"$eq": topic}}}))
