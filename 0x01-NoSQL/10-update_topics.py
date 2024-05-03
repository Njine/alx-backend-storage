#!/usr/bin/env python3
"""
Python function to update all topics in a school document based on the school's name.
"""

def update_topics(mongo_collection, name, topics):
    """
    Updates all topics for a school document identified by its name.

    Parameters:
    - mongo_collection: The pymongo collection object where the update will occur.
    - name: The name of the school whose topics are to be updated.
    - topics: A list of strings representing the new topics to set for the school.

    This function updates all documents with the given name, setting their "topics" field
    to the specified list of topics.
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
