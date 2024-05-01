#!/usr/bin/env python3
"""Module to implement a Redis-based cache with request tracking."""

from functools import wraps
from typing import Callable
import redis
import requests

# Create a Redis connection instance
redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator to count how many times a specific URL is requested.
    It caches the HTML content of the URL in Redis for faster subsequent retrievals.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """Increments the request count and uses cache if available."""
        redis_.incr(f"count:{url}")

        # Check if the content is already cached
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # If not cached, fetch the HTML content and cache it
        html_content = method(url)
        redis_.setex(f"cached:{url}", 10, html_content)
        
        return html_content

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Fetches the HTML content from a given URL.
    """
    response = requests.get(url)
    return response.text
