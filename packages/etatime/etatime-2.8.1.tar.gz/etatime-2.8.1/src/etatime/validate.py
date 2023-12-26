from dataclasses import dataclass
from typing import Any

class ValidationError(ValueError):
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(message)

@dataclass
class Validate:
    @staticmethod
    def type(value: Any, value_type: type) -> None:
        if not isinstance(value, value_type):
            raise ValidationError(f"Value '{value}' must be of type {value_type}, not {type(value)}")

    @staticmethod
    def positive(value: int | float) -> None:
        if value <= 0:
            raise ValidationError(f"Value '{value}' must be positive (non-zero)")

    @staticmethod
    def negative(value: int | float) -> None:
        if value >= 0:
            raise ValidationError(f"Value '{value}' must be negative (non-zero)")

    @staticmethod
    def non_positive(value: int | float) -> None:
        if value > 0:
            raise ValidationError(f"Value '{value}' must not be positive")

    @staticmethod
    def non_negative(value: int | float) -> None:
        if value < 0:
            raise ValidationError(f"Value '{value}' must not be negative")

    @staticmethod
    def range_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
        if value < minimum or value > maximum:
            raise ValidationError(f"Value '{value}' must be between {minimum} and {maximum} (inclusive)")

    @staticmethod
    def range_non_inclusive(value: int | float, minimum: int | float, maximum: int | float) -> None:
        if value <= minimum or value >= maximum:
            raise ValidationError(f"Value '{value}' must be between {minimum} and {maximum} (non-inclusive)")

    @staticmethod
    def gt(first: int | float, second: int | float) -> None:
        if not first > second:
            raise ValidationError(f"Value '{first}' must be greater than '{second}'")

    @staticmethod
    def gte(first: int | float, second: int | float) -> None:
        if not first >= second:
            raise ValidationError(f"Value '{first}' must be greater than or equal to '{second}'")

    @staticmethod
    def lt(first: int | float, second: int | float) -> None:
        if not first < second:
            raise ValidationError(f"Value '{first}' must be less than '{second}'")

    @staticmethod
    def lte(first: int | float, second: int | float) -> None:
        if not first <= second:
            raise ValidationError(f"Value '{first}' must be less than or equal to '{second}'")
