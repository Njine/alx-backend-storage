#!/usr/bin/env python3
"""Module containing decorators for call history, call counting, 
and a basic Cache class with Redis."""
import uuid
from functools import wraps
from typing import Callable, Optional, Union
import redis


def call_history(method: Callable) -> Callable:
    """
    Decorator that logs the history of a method's inputs and outputs.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Stores method's arguments and return value in Redis."""
        method_name = method.__qualname__
        self._redis.rpush(f"{method_name}:inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(f"{method_name}:outputs", str(result))
        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of a method's inputs and outputs from Redis.
    """
    method_name = method.__qualname__
    redis_db = method.__self__._redis
    inputs = redis_db.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_db.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        decoded_input = input.decode("utf-8")
        decoded_output = output.decode
