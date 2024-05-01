#!/usr/bin/env python3
"""Implements a Redis-based Cache class with decorators for tracking and counting operations."""

import uuid
from functools import wraps
from typing import Callable, Union, Optional
import redis


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    Uses the Redis `INCR` command to increment a count based on the method's qualified name.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increments the call count and returns the original method's result."""
        key = method.__qualname__  # Use the method's qualified name as the Redis key
        self._redis.incr(key)  # Increment the call count in Redis
        return method(self, *args, **kwargs)  # Return the result from the original method

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to track the history of a method's inputs and outputs.
    Records them in Redis lists for future retrieval and replay.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Stores the method's inputs and outputs in Redis lists."""
        method_name = method.__qualname__
        self._redis.rpush(f"{method_name}:inputs", str(args))  # Store inputs as a string
        result = method(self, *args, **kwargs)  # Call the original method
        self._redis.rpush(f"{method_name}:outputs", str(result))  # Store the output
        return result  # Return the output from the original method

    return wrapper


class Cache:
    """
    Redis-based Cache class to store and retrieve data.
    """

    def __init__(self) -> None:
        """Initializes a Redis connection and flushes the database."""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a randomly generated key and returns the key.
        """
        key = str(uuid.uuid4())  # Generate a unique key
        self._redis.set(key, data)  # Store the data in Redis
        return key  # Return the key used to store the data

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves the data from Redis using the given key.
        Applies a conversion function if provided. If the key doesn't exist, returns None.
        """
        value = self._redis.get(key)  # Retrieve data from Redis
        if value is not None and fn is not None:
            value = fn(value)  # Apply conversion function if provided
        return value  # Return the retrieved data

    def get_int(self, key: str) -> Optional[int]:
        """Retrieves the data from Redis as an integer."""
        return self.get(key, int)

    def get_str(self, key: str) -> Optional[str]:
        """Retrieves the data from Redis as a string."""
        return self.get(key, str)


def replay(method: Callable) -> None:
    """
    Displays the history of a method's inputs and outputs from Redis.
    """
    method_name = method.__qualname__
    inputs = self._redis.lrange(f"{method_name}:inputs", 0, -1)
    outputs = self._redis.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for decoded_input, decoded_output in zip(inputs, outputs):
        decoded_input = decoded_input.decode("utf-8")
        decoded_output = decoded_output.decode("utf-8")
        print(f"{method_name}(*{decoded_input}) -> {decoded_output}")
