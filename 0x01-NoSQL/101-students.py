#!/usr/bin/env python3
"""
Has top_students method.
"""
import pymongo


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    for student in mongo_collection.find():
        sum_of_scores = 0
        number_of_topics = 0
        for topic in student["topics"]:
            number_of_topics += 1
            sum_of_scores += topic["score"]
        mongo_collection.update_one(student,
                                    {"$set":
                                     {"averageScore":
                                      (sum_of_scores / number_of_topics)}})

    return mongo_collection.find().sort("averageScore", pymongo.DESCENDING)
