"""Provides tools for tracking, computing, and formatting time estimates."""
import datetime
from dataclasses import dataclass
from tqdm import tqdm

from etatime.time import TimeString
from etatime.constants import EtaDefaults


class EtaBar(tqdm):
    def __init__(
            self,
            *args,
            bar_format: str = "{l_bar}{bar}| {remainingS} | {etaS}",
            **kwargs):
        if "bar_format" in kwargs:
            del kwargs["bar_format"]
        super().__init__(*args, bar_format=bar_format, **kwargs)

        self.Stats.start_time = self.start_t

    @dataclass
    class Stats:
        start_time: float | None = None
        start_datetime: datetime.datetime | None = None
        current_time: float | None = None
        current_datetime: datetime.datetime | None = None
        elapsed_time: float | None = None
        elapsed_timedelta: datetime.timedelta | None = None
        remaining_time: float | None = None
        remaining_timedelta: datetime.timedelta | None = None
        eta_time: float | None = None
        eta_datetime: datetime.datetime | None = None
        initial: int | None = None
        total_items: int | None = None
        rate: float | None = None
        n: int | None = None
        percent: float | None = None

    @property
    def format_dict(self):
        d = super().format_dict

        # Extract useful information from the tqdm progress bar
        self.Stats.initial = d["initial"]
        self.Stats.n = d["n"]
        self.Stats.total_items = d["total"]
        self.Stats.elapsed_time = d["elapsed"]
        self.Stats.current_time = self.Stats.start_time + self.Stats.elapsed_time if self.Stats.start_time else None
        self.Stats.rate = d["rate"]

        if self.Stats.rate is None and self.Stats.elapsed_time:
            self.Stats.rate = (self.Stats.n - self.Stats.initial) / self.Stats.elapsed_time

        # Compute some values based on the tqdm source code
        self.Stats.remaining_time = (self.Stats.total_items - self.Stats.n) / self.Stats.rate if (
                self.Stats.rate and self.Stats.total_items) else None

        # Compute the ETA
        self.Stats.eta_time = self.Stats.current_time + self.Stats.remaining_time if (
                self.Stats.remaining_time and self.Stats.current_time) else None

        # Get the percent
        self.Stats.percent = self.Stats.n / self.Stats.total_items if self.Stats.total_items else None

        # Get the datetime objects
        self.Stats.start_datetime = datetime.datetime.fromtimestamp(self.Stats.start_time) if (
            self.Stats.start_time) else None
        self.Stats.current_datetime = datetime.datetime.fromtimestamp(self.Stats.current_time) if (
            self.Stats.current_time) else None
        self.Stats.elapsed_timedelta = datetime.timedelta(seconds=self.Stats.elapsed_time) if (
            self.Stats.elapsed_time) else None
        self.Stats.remaining_timedelta = datetime.timedelta(seconds=self.Stats.remaining_time) if (
            self.Stats.remaining_time) else None
        self.Stats.eta_datetime = datetime.datetime.fromtimestamp(self.Stats.eta_time) if (
            self.Stats.eta_time) else None

        # Add custom format codes
        start_string = TimeString.DateTime.short(self.Stats.start_datetime) if (
            self.Stats.start_datetime) else EtaDefaults.low_data_string
        start_string = f"S: {start_string}"
        d.update(startS=start_string)
        startL_string = TimeString.DateTime.long(self.Stats.start_datetime) if (
            self.Stats.start_datetime) else EtaDefaults.low_data_string
        startL_string = f"S: {startL_string}"
        d.update(startL=startL_string)

        current_string = TimeString.DateTime.short(self.Stats.current_datetime) if (
            self.Stats.current_datetime) else EtaDefaults.low_data_string
        current_string = f"C: {current_string}"
        d.update(currentS=current_string)
        currentL_string = TimeString.DateTime.long(self.Stats.current_datetime) if (
            self.Stats.current_datetime) else EtaDefaults.low_data_string
        currentL_string = f"C: {currentL_string}"
        d.update(currentL=currentL_string)

        elapsed_string = TimeString.TimeDelta.short(self.Stats.elapsed_timedelta) if (
            self.Stats.elapsed_timedelta) else EtaDefaults.low_data_string
        elapsed_string = f"E: {elapsed_string}"
        d.update(elapsedS=elapsed_string)
        elapsedL_string = TimeString.TimeDelta.long(self.Stats.elapsed_timedelta) if (
            self.Stats.elapsed_timedelta) else EtaDefaults.low_data_string
        elapsedL_string = f"E: {elapsedL_string}"
        d.update(elapsedL=elapsedL_string)

        remaining_string = TimeString.TimeDelta.short(self.Stats.remaining_timedelta) if (
            self.Stats.remaining_timedelta) else EtaDefaults.low_data_string
        remaining_string = f"R: {remaining_string}"
        d.update(remainingS=remaining_string)
        remainingL_string = TimeString.TimeDelta.long(self.Stats.remaining_timedelta) if (
            self.Stats.remaining_timedelta) else EtaDefaults.low_data_string
        remainingL_string = f"R: {remainingL_string}"
        d.update(elapsedL=remainingL_string)

        eta_string = TimeString.DateTime.short(self.Stats.eta_datetime) if (
            self.Stats.eta_datetime) else EtaDefaults.low_data_string
        eta_string = f"ETA: {eta_string}"
        d.update(etaS=eta_string)
        etaL_string = TimeString.DateTime.long(self.Stats.eta_datetime) if (
            self.Stats.eta_datetime) else EtaDefaults.low_data_string
        etaL_string = f"ETA: {etaL_string}"
        d.update(etaL=etaL_string)

        return d
