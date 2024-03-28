#!/usr/bin/env python3
"""
Has a Cache class.
"""
import redis
import uuid
from typing import Union
from functools import wraps


def count_calls(method):
    """
    Counts how many time the function is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Stores an instance of the Redis client.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key, stores the input data in Redis
        using the random key and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key, fn=None):
        """
        Takes a key string argument and an optional Callable argument named fn.
        This callable will be used to convert the data
        back to the desired format.
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, data):
        """
        Converts to string.
        """
        str(data)

    def get_int(self, data):
        """
        Converts to integer.
        """
        int(data)
