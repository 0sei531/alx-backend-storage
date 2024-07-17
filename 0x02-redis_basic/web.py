#!/usr/bin/env python3
""" Module for Implementing an Expiring Web Cache and Tracker using Redis """

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize Redis connection
redis_conn = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator for counting how many times a request has been made"""

    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper for decorator functionality"""
        redis_conn.incr(f"count:{url}")
        cached_html = redis_conn.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        html = method(url)
        redis_conn.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Fetch the HTML content of a particular URL"""
    req = requests.get(url)
    return req.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(get_page(url))  # This should fetch from cache
