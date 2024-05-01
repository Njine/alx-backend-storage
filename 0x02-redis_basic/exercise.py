#!/usr/bin/env python3
"""Redis-based Cache class and related decorators for tracking and caching operations."""

import uuid
from functools import wraps
from typing import Callable, Optional, Union
import redis


# Establish a Redis connection
redis_instance = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    Increments the count in Redis every time the method is invoked.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments call count."""
        redis_instance.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to record the history of a method's inputs and outputs.
    Stores the inputs and outputs in Redis lists.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Records input and output for the wrapped method."""
        method_name = method.__qualname__
        # Store input arguments as a string in the inputs list
        redis_instance.rpush(f"{method_name}:inputs", str(args))
        # Get output by calling the original method
        output = method(self, *args, **kwargs)
        # Store output in the outputs list
        redis_instance.rpush(f"{method_name}:outputs", str(output))
        return output

    return wrapper


class Cache:
    """
    Cache class for storing and retrieving data using Redis.
    """

    def __init__(self) -> None:
        """Initializes a Redis instance and flushes the database."""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in Redis with a randomly generated key.
        Returns the key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves the value from Redis for a given key.
        If a conversion function is provided, it applies it to the retrieved value.
        If the key does not exist, it returns None.
        """
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves the value from Redis and converts it to an integer.
        """
        return self.get(key, int)

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves the value from Redis and converts it to a string.
        """
        return self.get(key, str)


def replay(method: Callable) -> None:
    """
    Displays the call history for a specific method, including inputs and outputs.
    """
    method_name = method.__qualname__
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        decoded_input = input.decode("utf-8")
        decoded_output = output.decode("utf-8")
        print(f"{method_name}(*{decoded_input}) -> {decoded_output}")
