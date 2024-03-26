#!/usr/bin/env python3
"""
Has the insert_school function.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into a collection(mongo_collection) based on kwargs.
    Returns the new _id.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
