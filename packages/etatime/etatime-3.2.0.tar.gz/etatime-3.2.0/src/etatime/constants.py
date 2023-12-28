"""Contains constants used in by other components of the module."""
from typing import ClassVar
from dataclasses import dataclass


@dataclass
class EtaDefaults:
    """The defaults to use for the `eta` submodule."""
    low_data_string: ClassVar[str] = "???"
