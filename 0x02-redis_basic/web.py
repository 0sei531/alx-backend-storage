#!/usr/bin/env python3
""" Advanced - Module for Implementing an expiring web cache and tracker """
import redis
import requests
from typing import Callable
from functools import wraps


def count_requests(method: Callable) -> Callable:
    """ Counting with decorators how many times a request has been made """
    @wraps(method)
    def wrapper(url: str) -> str:
        """ Wrapper for decorator functionality """
        redis_client = redis.Redis()
        redis_client.incr(f"count:{url}")
        cached_html = redis_client.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_client.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a particular URL and returns it. """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching {url}: {str(e)}"


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
