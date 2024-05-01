#!/usr/bin/env python3
"""Web cache with request tracking and caching using Redis."""

import redis
import requests
from functools import wraps
from typing import Callable

# Establish a Redis connection
redis_instance = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is accessed.
    It also caches the result with an expiration time.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """Increments the request count and uses cached content if available."""
        # Increment the request count in Redis for the given URL
        redis_instance.incr(f"count:{url}")

        # Check if the HTML content is cached
        cached_html = redis_instance.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode("utf-8")

        # Fetch HTML content and cache it with an expiration time of 10 seconds
        html_content = method(url)
        redis_instance.setex(f"cached:{url}", 10, html_content)

        return html_content

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Retrieves the HTML content from a given URL.
    Uses caching and tracks request count in Redis.
    """
    response = requests.get(url)
    return response.text
