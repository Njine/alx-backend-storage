#!/usr/bin/env python3
"""Implements a simple web cache with request tracking using Redis."""

from functools import wraps
from typing import Callable
import redis
import requests


# Establish a Redis connection
redis_instance = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is accessed.
    Also implements caching for faster retrieval of HTML content.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """Increment the request count and use cached content if available."""
        redis_instance.incr(f"count:{url}")

        # Check if the content is cached
        cached_html = redis_instance.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode("utf-8")

        # If not cached, fetch the HTML content and cache it
        html_content = method(url)
        redis_instance.setex(f"cached:{url}", 10, html_content)

        return html_content

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Fetches the HTML content from a given URL and caches it with an expiration time.
    """
    response = requests.get(url)
    return response.text
