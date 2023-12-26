"""Contains constants used in by other components of the module."""
from typing import ClassVar
from dataclasses import dataclass
from pydantic import NonNegativeInt, PositiveInt


@dataclass
class EtaDefaults:
    """The defaults to use for the `eta` submodule."""
    verbose: ClassVar[bool] = False
    percent_completion: ClassVar[NonNegativeInt] = 2
    not_enough_data_string: ClassVar[str] = "not enough data"
    sep: ClassVar[str] = " | "
    invalid_string_type_string = "invalid string type requested"


@dataclass
class TimeDefaults:
    """The defaults to use for the `time` submodule."""
    unknown_format_string: ClassVar[str] = "unknown time format"

@dataclass
class CompletionDefaults:
    """The defaults to use for the `completion` submodule."""
    width: ClassVar[PositiveInt] = 5
