#!/usr/bin/env python3
"""
Has the schools_by_topic function.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic.
    """
    result = mongo_collection.find({"topics": topic})

    return result
