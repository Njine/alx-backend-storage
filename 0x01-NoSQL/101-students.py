#!/usr/bin/env python3
"""
A Python function that returns all students sorted by average score.
"""

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Parameters:
    - mongo_collection: The pymongo collection object to query.

    Returns:
    - A list of students, with each item containing the student's name, _id, and averageScore.
    """
    return list(mongo_collection.aggregate([
        {
            "$unwind": "$topics"  # Decompose the 'topics' array to access individual scores
        },
        {
            "$group": {
                "_id": {"_id": "$_id", "name": "$name"},  # Group by _id and name
                "averageScore": {"$avg": "$topics.score"}  # Compute the average score
            }
        },
        {
            "$project": {
                "_id": "$_id._id",  # Restore the _id
                "name": "$_id.name",
                "averageScore": "averageScore"
            }
        },
        {
            "$sort": {
                "averageScore": -1  # Sort by average score in descending order
            }
        }
    ]))
