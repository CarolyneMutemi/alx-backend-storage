#!/usr/bin/env python3
"""
Lists all documents in a collection.
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    Returns an empty lis if no document is found.
    """
    document_list = []
    for doc in mongo_collection.find():
        document_list.append(doc)

    return document_list
