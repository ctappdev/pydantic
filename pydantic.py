"""
Pydantic Tutorial by Arjan Codes
"""

import json
from typing import List, Optional

import pydantic


class ISBN10FormatError(Exception):
    """Custom error handler for ISBN_10 format errors"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Book(pydantic.BaseModel):
    title: str
    author: str
    publisher: str
    price: float
    isbn_10: Optional[str]
    isbn_13: Optional[str]
    subtitle: Optional[str]

    @pydantic.validator("isbn_10")
    @classmethod
    def validate_isbn_10(cls, value) -> None:
        print(f"Validate {value}")
        chars = [c for c in value if c in "0123456789Xx"]
        if len(chars) != 10:
            raise ISBN10FormatError(
                value=value, message="ISBN 10 should contain 10 digits"
            )

        def char_to_int(char: str):
            if char in ("Xx"):
                return 10
            return int(char)

        weighted_sum = sum((10 - i) * char_to_int(x) for i, x in enumerate(chars))
        if weighted_sum % 11 != 0:
            raise ISBN10FormatError(
                value=value, message="ISBN 10 digit sum should be divisble by 11"
            )

        return value


# Read data from JSON file
with open("./data.json") as file:
    data = json.load(file)
    books: List[Book] = [Book(**item) for item in data]

    print(books[0].publisher)
