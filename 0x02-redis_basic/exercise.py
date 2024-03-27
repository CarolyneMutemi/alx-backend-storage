#!/usr/bin/env python3
"""
Has a Cache class.
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    Stores an instance of the Redis client.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key, stores the input data in Redis
        using the random key and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
