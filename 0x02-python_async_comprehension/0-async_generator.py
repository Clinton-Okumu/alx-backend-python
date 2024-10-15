#!/usr/bin/env python3
""" a python module to loop 10 times """
import random
import asyncio
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    """
    async_generator - function to loop 10 times
    Arguments:
        no arguments
    Returns:
        AsyncGenerator yielding random float values
    """
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
