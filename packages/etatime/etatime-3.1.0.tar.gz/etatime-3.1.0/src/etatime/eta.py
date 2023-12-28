"""Provides tools for tracking, computing, and formatting time estimates."""
import datetime
from typing import Any, Iterator, Iterable, Generator
from tqdm import tqdm

from etatime.time import TimeString
from etatime.constants import EtaDefaults


class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


class EtaBar:
    def __init__(
            self,
            items: Iterable[Any],
            bar_format: str = "{l_bar}{bar}{r_bar}",
            **kwargs
    ):
        self.bar_format = bar_format

        self.pbar = tqdm(items, **kwargs)

        self._initial = self.pbar.initial
        self._start_t = self.pbar.start_t

        self.total_items = None
        self.rate = None
        self.n = None

        self.percent = None

        self.start_time = datetime.datetime.fromtimestamp(self._start_t)
        self.current_time = None
        self.elapsed_time = None
        self.remaining_time = None
        self.eta_time = None

    def _make_eta_bar_format(
            self
    ):
        preformat_dict = {
            "r_bar": "| ({n_fmt}/{total_fmt}) | R: {remaining} | ETA: {eta}",
            "r_barL": "| ({n_fmt}/{total_fmt}) | Remaining: {remainingL} | ETA: {etaL}"
        }
        preformatted_text = self.bar_format.format_map(SafeDict(**preformat_dict))

        format_dict = {
            "start": TimeString.DateTime.short(self.start_time),
            "startL": TimeString.DateTime.long(self.start_time),
            "current": TimeString.DateTime.short(
                self.current_time) if self.current_time else EtaDefaults.low_data_string,
            "currentL": TimeString.DateTime.long(
                self.current_time) if self.current_time else EtaDefaults.low_data_string,
            "elapsed": TimeString.TimeDelta.short(
                self.elapsed_time) if self.elapsed_time else EtaDefaults.low_data_string,
            "elapsedL": TimeString.TimeDelta.long(
                self.elapsed_time) if self.elapsed_time else EtaDefaults.low_data_string,
            "remaining": TimeString.TimeDelta.short(
                self.remaining_time) if self.remaining_time else EtaDefaults.low_data_string,
            "remainingL": TimeString.TimeDelta.long(
                self.remaining_time) if self.remaining_time else EtaDefaults.low_data_string,
            "eta": TimeString.DateTime.short(
                self.eta_time) if self.eta_time else EtaDefaults.low_data_string,
            "etaL": TimeString.DateTime.long(
                self.eta_time) if self.eta_time else EtaDefaults.low_data_string
        }

        formatted_text = preformatted_text.format_map(SafeDict(**format_dict))

        return formatted_text

    def update(self, n: int = None):
        if n is None:
            self.n = self.pbar.n
        else:
            self.n = n
            self.pbar.update(self.n)

        self.pbar.bar_format = self._make_eta_bar_format()

        # Extract useful information from the tqdm progress bar
        self.total_items = self.pbar.total
        current_t = self.pbar.last_print_t

        # Compute some values based on the tqdm source code
        elapsed_t = current_t - self._start_t if current_t else 0
        self.rate = (self.n - self._initial) / elapsed_t if elapsed_t else None
        remaining_t = (self.total_items - self.n) / self.rate if self.rate and self.total_items else None

        # Compute the ETA
        eta_t = current_t + remaining_t if remaining_t else None

        # Get the percent
        self.percent = self.n / self.total_items if self.total_items else None

        # Get datetimes from timestamps
        self.current_time = datetime.datetime.fromtimestamp(current_t) if current_t else None
        self.elapsed_time = datetime.timedelta(seconds=elapsed_t)
        self.remaining_time = datetime.timedelta(seconds=remaining_t) if remaining_t else None
        self.eta_time = datetime.datetime.fromtimestamp(eta_t) if eta_t else None

    def __iter__(self):
        try:
            for item in self.pbar:
                self.update()
                yield item
        finally:
            self.update()
