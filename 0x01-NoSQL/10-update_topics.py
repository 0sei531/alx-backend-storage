#!/usr/bin/env python3
""" Write a Python function that changes all topics of a school
    document based on the name
"""
def update_topics(mongo_collection, name, topics):
    """
    Update topics of all school documents that match the name.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The collection object to update.
        name (str): The name of the school whose topics are to be updated.
        topics (list of str): The new list of topics to set for the school.

    Returns:
        None
    """
    query = {"name": name}
    new_values = {"$set": {"topics": topics}}

    # Check if there are documents matching the query
    count = mongo_collection.count_documents(query)
    if count == 0:
        print(f"No documents found with name '{name}' to update.")
        return

    mongo_collection.update_many(query, new_values)
