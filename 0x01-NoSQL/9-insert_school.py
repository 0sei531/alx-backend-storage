#!/usr/bin/env python3
""" Write a Python function that inserts a new document in a collection based on kwargs """


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into a MongoDB collection based
    on provided keyword arguments.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The collection object to insert into.
        **kwargs: Keyword arguments representing fields and
        values for the new document.

    Returns:
        str: The _id of the newly inserted document.
    """
    # Insert the document and get the inserted _id
    result = mongo_collection.insert_one(kwargs)
    new_school_id = result.inserted_id
    return str(new_school_id)
