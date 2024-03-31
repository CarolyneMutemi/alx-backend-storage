#!/usr/bin/env python3
"""
Implenting an expiring web cache and tracker.
"""
from functools import wraps
import requests
import redis


def count_requests(method):
    """
    Tracks how many times a particular URL was accessed.
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper function.
        """
        connection = redis.Redis()
        connection.incr(f"count:{url}")
        connection.expire(f"count:{url}", 10)
        print(connection.get(f"count:{url}"), connection.ttl(f"count:{url}"))
        return method(url)
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Get's html content of the given url.
    """
    content = requests.get(url, timeout=5).text
    return content
