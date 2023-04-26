"""
Validation and message constants
"""
from enum import Enum


class Messages(Enum):
    """
    Message constants that will be shown at frontend.
    """

    pass


# validation regex
EMAIL_VALIDATION_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
