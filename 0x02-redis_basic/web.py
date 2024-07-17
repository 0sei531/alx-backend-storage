#!/usr/bin/env python3
"""
Implements an expiring web cache and tracker
"""

import redis
import requests
from functools import wraps
from typing import Callable


redis_client = redis.Redis()


def cache_with_expiration(expiration_time: int = 10) -> Callable:
    """
    Decorator to cache the result of a function with expiration time
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Increment the access count for the URL
            redis_client.incr(f"count:{url}")

            # Check if the page is cached
            cached_page = redis_client.get(f"cached:{url}")
            if cached_page:
                return cached_page.decode('utf-8')

            # If not cached, call the original function
            result = func(url)

            # Cache the result with expiration time
            redis_client.setex(f"cached:{url}", expiration_time, result)

            return result
        return wrapper
    return decorator


@cache_with_expiration()
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    page_content = get_page(url)
    print(page_content)
    print(f"Number of accesses: {redis_client.get(f'count:{url}').decode('utf-8')}")
