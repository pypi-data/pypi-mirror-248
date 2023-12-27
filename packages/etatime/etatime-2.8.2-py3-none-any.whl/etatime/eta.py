"""Provides tools for tracking, computing, and formatting time estimates."""
import sys
import datetime
from enum import Enum
from typing import Any, Iterator, Sequence

from etatime.completion import Completion
from etatime.time import TimeString
from etatime.constants import EtaDefaults, CompletionDefaults
from etatime.validate import Validate


class EtaValue(Enum):
    """An enum with attributes representing the values of an Eta object."""
    TOTAL_ITEMS = 1
    ITEM_INDEX = 2
    START_TIME = 3
    CURRENT_TIME = 4
    ETA = 5
    TIME_REMAINING = 6
    COMPLETION = 7
    TIME_TAKEN = 8


class Eta:
    """Data class to hold, compute, and format ETA state information and time estimate info.

    :param int total_items: The total number of items to process, used in computations.
    :param int item_index: The index of the item about to be processed (0-indexed).
    :param datetime.datetime start_time: The starting time to use for the computation.
    :param current_time: The time to use for the computation, defaults to the current time.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :param str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :ivar int total_items: The total number of items to process, used in computations.
    :ivar int item_index: The index of the item about to be processed (0-indexed).
    :ivar datetime.datetime start_time: The starting time to use for the computation.
    :ivar datetime.datetime current_time: The time to use for the computation.
    :ivar datetime.datetime eta: The estimated completion time.
    :ivar datetime.timedelta time_remaining: The time remaining.
    :ivar float completion: The completion percentage.
    :ivar datetime.timedelta time_taken: The time taken.

    :raises ValidationError: Raised when a parameter is invalid.
    """
    def __init__(
            self,
            total_items: int,
            item_index: int,
            start_time: datetime.datetime,
            current_time: datetime.datetime = None,
            verbose: bool = EtaDefaults.verbose,
            percent_decimals: int = EtaDefaults.percent_completion,
            not_enough_data_string: str = EtaDefaults.not_enough_data_string
    ):
        Validate.gte(total_items, 2)
        Validate.non_negative(item_index)
        Validate.non_negative(percent_decimals)

        if current_time is None:
            current_time = datetime.datetime.now()

        self.total_items = total_items
        self.item_index = item_index
        self.start_time = start_time
        self.current_time = current_time
        self.verbose = verbose
        self.percent_decimals = percent_decimals
        self.not_enough_data_string = not_enough_data_string

        self._validate_item_index(self.item_index)

        self.verbose = verbose
        self.eta = self._eta()
        self.time_remaining = self._time_remaining()
        self.completion = self._completion()
        self.time_taken = self._time_taken()

    def __str__(self) -> str:
        """Returns the string format of this ETA object.

        :return: The user-friendly progress string.
        :rtype: str
        """
        return self.progress_string()

    def __repr__(self) -> str:
        """Returns the string format of this ETA object.

        :return: The user-friendly progress string.
        :rtype: str
        """
        return self.statistics_string()

    def _validate_item_index(
            self,
            item_index: int
    ) -> None:
        """Validate that an index is not larger than the total items and raise an IndexError otherwise.

        Index type and positivity are not validated in this private method because pydantic handles it elsewhere.

        :param int item_index: The index to test.

        :raises IndexError: Raised when the index is too large.

        :rtype: None
        """
        Validate.range_inclusive(item_index, 0, self.total_items - 1)

    def _eta(self) -> datetime.datetime | None:
        """Compute the ETA and return it as a datetime.datetime object.

        :return: The ETA as a datetime.datetime object.
        :rtype: datetime.datetime
        """
        time_remaining = self._time_remaining()
        if time_remaining is None:
            return None

        return self.current_time + time_remaining

    def _time_remaining(self) -> datetime.timedelta | None:
        """Compute the time remaining and return it as a datetime.timedelta object.

        :return: The time remaining as a datetime.timedelta object, None if the index is 0.
        :rtype: datetime.timedelta | None
        """
        percent_done = self._completion()
        if percent_done <= 0:
            return None

        progress_scale = (1 - percent_done) / percent_done

        return self._time_taken() * progress_scale

    def _completion(self) -> float:
        """Compute the completion percentage and return it as a float.

        :return: The completion percentage as a float in range on 0.0 - 1.0.
        :rtype: float
        """
        return Completion(
                    total=self.total_items,
                    index=self.item_index
                ).value()

    def _time_taken(self) -> datetime.timedelta:
        """Compute the time taken and return it as a datetime.timedelta object.

        :return: The time taken as a datetime.timedelta object.
        :rtype: datetime.timedelta
        """
        return self.current_time - self.start_time

    def string(
            self,
            field: EtaValue,
            verbose: bool = None
    ) -> str:
        """Convert a specific field of this object into a human-readable string.

        :param Field field: The specific field to convert to a string.
        :param bool verbose: If set, override the default verbosity.

        :return: The human-readable string for the specified field.
        :rtype: str
        """
        if verbose is None:
            verbose = self.verbose

        match field:
            case EtaValue.START_TIME:
                field_string = TimeString.automatic(
                    time_in=self.start_time,
                    verbose=verbose
                )
            case EtaValue.CURRENT_TIME:
                field_string = TimeString.automatic(
                    time_in=self.start_time,
                    verbose=verbose
                )
            case EtaValue.TIME_REMAINING:
                if self.time_remaining is None:
                    field_string = self.not_enough_data_string
                else:
                    field_string = TimeString.automatic(
                        time_in=self.time_remaining,
                        verbose=verbose
                    )
            case EtaValue.TIME_TAKEN:
                field_string = TimeString.automatic(
                    time_in=self.time_taken,
                    verbose=verbose
                )
            case EtaValue.ETA:
                if self.eta is None:
                    field_string = self.not_enough_data_string
                else:
                    field_string = TimeString.automatic(
                        time_in=self.eta,
                        verbose=verbose
                    )
            case EtaValue.COMPLETION:
                field_string = Completion(
                    total=self.total_items,
                    index=self.item_index
                ).string(
                    decimals=self.percent_decimals,
                    verbose=verbose
                )
            case EtaValue.TOTAL_ITEMS:
                field_string = str(self.total_items)
            case EtaValue.ITEM_INDEX:
                field_string = str(self.item_index)
            case _:
                field_string = EtaDefaults.invalid_string_type_string

        return field_string

    def progress_string(
            self,
            sep: str = EtaDefaults.sep,
            verbose: bool = None
    ) -> str:
        """Combine the most useful stats into a string focused on conveying progress and return it.

        :param str sep: The string to use as a seperator between fields.
        :param bool verbose: If set, override the default verbosity.

        :raises pydantic.ValidationError: Raised when a parameter is invalid.

        :return: A human-readable string that includes (in order) completion, time remaining, and ETA.
        :rtype: str
        """
        if verbose is None:
            verbose = self.verbose

        completion_string = self.string(EtaValue.COMPLETION, verbose=verbose)

        if self.item_index <= 0:
            return completion_string

        difference_string = self.string(EtaValue.TIME_REMAINING, verbose=verbose)
        eta_string = self.string(EtaValue.ETA, verbose=verbose)
        if verbose:
            difference_string = f"Time remaining: {difference_string}"
            eta_string = f"ETA: {eta_string}"
        else:
            difference_string = f"R: {difference_string}"
            eta_string = f"E: {eta_string}"

        return sep.join([completion_string, difference_string, eta_string])

    def statistics_string(
            self,
            sep: str = EtaDefaults.sep,
            verbose: bool = None
    ) -> str:
        """Combine all the stats into a string focused on conveying everything useful about this object.

        :param str sep: The string to use as a seperator between fields.
        :param bool verbose: If set, override the default verbosity.

        :raises pydantic.ValidationError: Raised when a parameter is invalid.

        :return: A human-readable string that includes all useful statistics about this object.
        :rtype: str
        """
        if verbose is None:
            verbose = self.verbose

        time_taken_string = self.string(EtaValue.TIME_TAKEN, verbose=verbose)
        start_time_string = self.string(EtaValue.START_TIME, verbose=verbose)
        current_time_string = self.string(EtaValue.CURRENT_TIME, verbose=verbose)

        if self.verbose:
            time_taken_string = f"Time taken: {time_taken_string}"
            start_time_string = f"Start time: {start_time_string}"
            current_time_string = f"Time of estimation: {current_time_string}"
        else:
            time_taken_string = f"T: {time_taken_string}"
            start_time_string = f"S: {start_time_string}"
            current_time_string = f"C: {current_time_string}"

        return sep.join([
            self.progress_string(verbose=verbose),
            start_time_string,
            current_time_string,
            time_taken_string
        ])

    def complete(
            self,
            current_time: datetime.datetime = None,
    ) -> None:
        """Set the ETA item to completed (100%).

        :param datetime.datetime current_time: The time to use for the computation, defaults to the current time.

        :rtype: None
        """
        if current_time is None:
            current_time = datetime.datetime.now()

        self.item_index = self.total_items
        self.current_time = current_time

        self.eta = current_time
        self.time_remaining = datetime.timedelta(0)
        self.completion = self._completion()
        self.time_taken = self._time_taken()


class EtaCalculator:
    """Tracks, computes, and formats time estimates.

    :param int total_items: The total number of items to process, used in computations.
    :param datetime.datetime start_time: The starting time used in all calculations, defaults to the current time.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :param str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :ivar int total_items: The total number of items to process, used in computations.
    :ivar datetime.datetime start_time: The starting time used in all calculations, defaults to the current time.
    :ivar bool verbose: If we should make strings verbosely or not.
    :ivar int percent_decimals: The number of decimal places to use in the percentage string.
    :ivar str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :raises pydantic.ValidationError: Raised when a parameter is invalid.
    """
    def __init__(
            self,
            total_items: int,
            start_time: datetime.datetime = None,
            verbose: bool = EtaDefaults.verbose,
            percent_decimals: int = EtaDefaults.percent_completion,
            not_enough_data_string: str = EtaDefaults.not_enough_data_string
    ):
        Validate.gte(total_items, 2)
        Validate.non_negative(percent_decimals)

        if start_time is None:
            start_time = datetime.datetime.now()

        self.total_items = total_items
        self.start_time = start_time
        self.verbose = verbose
        self.percent_decimals = percent_decimals
        self.not_enough_data_string = not_enough_data_string

        self.eta = None
        self.update_eta(item_index=0, current_time=start_time)

    def __str__(self) -> str:
        """Return the string format of this ETA calculator object.

        :return: The user-friendly string representing the calculator object.
        :rtype: str
        """
        return (f"ETA calculator for {self.total_items} items, "
                f"start time = {self.start_time}, "
                f"verbose = {self.verbose}, "
                f"percentage decimal places = {self.percent_decimals}")

    def __repr__(self) -> str:
        """Return the string format of this ETA calculator object.

        :return: The user-friendly string representing the calculator object.
        :rtype: str
        """
        return self.__str__()

    def update_eta(
            self,
            item_index: int,
            current_time: datetime.datetime = None
    ) -> None:
        """Get the current ETA calculation and set self.eta to it.

        :param int item_index: The index of the item about to be processed (0-indexed).
        :param datetime.datetime current_time: The time to use for the computation, defaults to the current time.

        :raises ValidationError: Raised when a parameter is invalid.

        :rtype: None
        """
        Validate.range_inclusive(item_index, 0, self.total_items - 1)

        if current_time is None:
            current_time = datetime.datetime.now()

        self.eta = Eta(
            total_items=self.total_items,
            item_index=item_index,
            start_time=self.start_time,
            current_time=current_time,
            verbose=self.verbose,
            percent_decimals=self.percent_decimals
        )

    def complete(
            self,
            current_time: datetime.datetime = None
    ) -> None:
        if current_time is None:
            current_time = datetime.datetime.now()

        if self.eta is not None:
            self.eta.complete()
        else:
            self.eta = Eta(
            total_items=self.total_items,
            item_index=self.total_items - 1,
            start_time=self.start_time,
            current_time=current_time,
            verbose=self.verbose,
            percent_decimals=self.percent_decimals
        )


class eta_calculator:
    """Decorates an iterable and returns an identical iterator, but with progress tracking.

    :param Sequence[Any] items: The sequence to iterate over.
    :param datetime.datetime start_time: The starting time to use for the computation, defaults to now.
    :param bool verbose: If we should make strings verbosely or not.
    :param int percent_decimals: The number of decimal places to use in the percentage string.
    :param str not_enough_data_string: The string to return when there is not enough data for the desired computation.

    :return: an identical iterator, but with progress tracking in the computed self.eta attribute.
    :rtype: Iterator[Any]
    """
    def __init__(
            self,
            items: Sequence[Any],
            start_time: datetime.datetime = None,
            verbose: bool = EtaDefaults.verbose,
            percent_decimals: int = EtaDefaults.percent_completion,
            not_enough_data_string: str = EtaDefaults.not_enough_data_string,
            sep: str = EtaDefaults.sep
    ):
        Validate.non_negative(percent_decimals)

        if start_time is None:
            start_time = datetime.datetime.now()

        self.items = items
        self.start_time = start_time
        self.verbose = verbose
        self.sep = sep

        self.calculator = EtaCalculator(
            total_items=len(items),
            start_time=start_time,
            verbose=verbose,
            percent_decimals=percent_decimals,
            not_enough_data_string=not_enough_data_string,
        )

        self.eta = self.calculator.eta

    def complete(
            self,
            current_time: datetime.datetime = None
    ) -> None:
        if current_time is None:
            current_time = datetime.datetime.now()

        if self.eta is not None:
            self.eta.complete(current_time=current_time)

    def __iter__(self):
        self.total_items = len(self.items)
        self.last_index = -1

        return self

    def __next__(self):
        index = self.last_index + 1
        if index < self.total_items:
            self.calculator.update_eta(index)
            self.eta = self.calculator.eta

            self.last_index = index

            return self.items[index]

        self.complete()

        raise StopIteration


class eta_bar:
    def __init__(
            self,
            items: Sequence[Any],
            start_time: datetime.datetime = None,
            verbose: bool = EtaDefaults.verbose,
            percent_decimals: int = EtaDefaults.percent_completion,
            not_enough_data_string: str = EtaDefaults.not_enough_data_string,
            sep: str = EtaDefaults.sep,
            width: int = CompletionDefaults.width,
            file = sys.stderr
    ):
        Validate.non_negative(percent_decimals)
        Validate.positive(width)

        if start_time is None:
            start_time = datetime.datetime.now()

        self.items = items
        self.start_time = start_time
        self.verbose = verbose
        self.sep = sep
        self.width = width
        self.file = file

        self.calculator = EtaCalculator(
            total_items=len(items),
            start_time=start_time,
            verbose=verbose,
            percent_decimals=percent_decimals,
            not_enough_data_string=not_enough_data_string
        )

    def write(
            self,
            value,
            overwrite=False
    ):
        if overwrite:
            print("", end=f"\r{value}", file=self.file)
            # print(value, file=self.file)
        else:
            print(value, file=self.file)

    def bar(
            self,
            index
    ):
        bar = Completion(
            total=self.eta.total_items,
            index=index
        ).bar(
            width=self.width
        )
        bar = f"|{bar}|"

        return bar

    def complete(
            self,
            current_time: datetime.datetime = None
    ) -> None:
        if current_time is None:
            current_time = datetime.datetime.now()

        if self.eta is not None:
            self.eta.complete(current_time=current_time)

    def __iter__(self):
        self.eta = self.calculator.eta
        self.total_items = len(self.items)
        self.last_message_length = 0
        self.last_index = -1

        return self

    def __next__(self) -> Iterator[Any]:
        index = self.last_index + 1
        if index < self.total_items:
            self.calculator.update_eta(index)
            self.eta =  self.calculator.eta

            bar = self.bar(index)

            message = f"{bar} {self.eta.progress_string(sep=self.sep)}"
            self.write(" " * self.last_message_length, overwrite=True)
            self.write(message, overwrite=True)

            self.last_message_length = len(message)
            self.last_index = index

            return self.items[index]

        self.complete()

        bar = self.bar(index)
        time_taken_string = self.eta.string(EtaValue.TIME_TAKEN)
        end_time_string = self.eta.string(EtaValue.CURRENT_TIME)
        if self.verbose:
            time_taken_string = f"Time taken: {time_taken_string}"
            end_time_string = f"Completion time: {end_time_string}"
        else:
            time_taken_string = f"T: {time_taken_string}"
            end_time_string = f"C: {end_time_string}"

        completion_string = self.eta.string(EtaValue.COMPLETION)

        end_stats_string = self.sep.join([completion_string, time_taken_string, end_time_string])
        self.write(f"{bar} {end_stats_string}\n", overwrite=True)

        raise StopIteration
