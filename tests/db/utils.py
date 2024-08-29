"""
Random test utils
"""

# Builtin imports
import time
from random import randbytes

def get_random_email_address() -> str:
    """
    Returns a random email address
    """
    return f"{time.time()}@example.com"
