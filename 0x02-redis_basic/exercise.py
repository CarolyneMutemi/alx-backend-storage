#!/usr/bin/env python3
"""
Has a Cache class.
"""
import uuid
from typing import Union, Callable, ParamSpec, TypeVar
from functools import wraps
import redis
P = ParamSpec('P')
T = TypeVar('T')


def count_calls(method: Callable[P, T]) -> Callable[P, T]:
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


def call_history(method: Callable[P, T]) -> Callable[P, T]:
    """
    Stores the history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
    return wrapper


def replay(func):
    """
    Displays the history calls of a particular function.
    """
    number_of_calls = (func.__self__._redis.get(func.__qualname__)
                       ).decode('utf-8')
    print(f"{func.__qualname__} was called {number_of_calls} times:")
    inputs = func.__self__._redis.lrange(f"{func.__qualname__}:inputs", 0, -1)
    outputs = func.__self__._redis.lrange(f"{func.__qualname__}:outputs",
                                          0, -1)
    for (value, output) in zip(inputs, outputs):
        value = value.decode('utf-8')
        output = output.decode('utf-8')
        print(f"{func.__qualname__}(*{value}) -> {output}")


class Cache:
    """
    Stores an instance of the Redis client.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
