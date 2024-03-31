#!/usr/bin/env python3
"""
Implenting an expiring web cache and tracker.
"""
import requests
import redis


# def count_requests(method):
#     """
#     Tracks how many times a particular URL was accessed.
#     """
#     @wraps(method)
#     def wrapper(url):
#         """
#         Wrapper function.
#         """
#         connection = redis.Redis()
#         page = connection.get("page")
#         if not page:
#             page = method(url)
#             connection.setex("page", 10, page)
#         else:
#             page = page.decode('utf-8')
#         connection.incr(f"count:{url}")
#         return page
#     return wrapper


def get_page(url: str) -> str:
    """
    Get's html content of the given url.
    """
    connection = redis.Redis()
    page = connection.get("page")
    if not page:
        page = requests.get(url, timeout=5).text
        connection.setex("page", 10, page)
    else:
        page = page.decode('utf-8')
    connection.incr(f"count:{url}")
    print(connection.get(f"count:{url}"))
    print(page)
    return page
