"""Provides tools for tracking, computing, and formatting time estimates."""
import datetime
from dataclasses import dataclass
from tqdm import tqdm

from etatime.time import TimeString
from etatime.constants import EtaDefaults


@dataclass
class EtaStats:
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


class EtaBar(tqdm):
    def __init__(
            self,
            *args,
            bar_format: str = "{l_bar}{bar}| {remainingS} | {etaS}",
            **kwargs):
        if "bar_format" in kwargs:
            del kwargs["bar_format"]
        super().__init__(*args, bar_format=bar_format, **kwargs)
        
        self.stats = EtaStats()

        self.stats.start_time = self.start_t

    @property
    def format_dict(self):
        d = super().format_dict

        # Extract useful information from the tqdm progress bar
        self.stats.initial = d["initial"]
        self.stats.n = d["n"]
        self.stats.total_items = d["total"]
        self.stats.elapsed_time = d["elapsed"]
        self.stats.current_time = self.stats.start_time + self.stats.elapsed_time if self.stats.start_time else None
        self.stats.rate = d["rate"]

        if self.stats.rate is None and self.stats.elapsed_time:
            self.stats.rate = (self.stats.n - self.stats.initial) / self.stats.elapsed_time

        # Compute some values based on the tqdm source code
        self.stats.remaining_time = (self.stats.total_items - self.stats.n) / self.stats.rate if (
                self.stats.rate and self.stats.total_items) else None

        # Compute the ETA
        self.stats.eta_time = self.stats.current_time + self.stats.remaining_time if (
                self.stats.remaining_time and self.stats.current_time) else None

        # Get the percent
        self.stats.percent = self.stats.n / self.stats.total_items if self.stats.total_items else None

        # Get the datetime objects
        self.stats.start_datetime = datetime.datetime.fromtimestamp(self.stats.start_time) if (
            self.stats.start_time) else None
        self.stats.current_datetime = datetime.datetime.fromtimestamp(self.stats.current_time) if (
            self.stats.current_time) else None
        self.stats.elapsed_timedelta = datetime.timedelta(seconds=self.stats.elapsed_time) if (
            self.stats.elapsed_time) else None
        self.stats.remaining_timedelta = datetime.timedelta(seconds=self.stats.remaining_time) if (
            self.stats.remaining_time) else None
        self.stats.eta_datetime = datetime.datetime.fromtimestamp(self.stats.eta_time) if (
            self.stats.eta_time) else None

        # Add custom format codes
        start_string = TimeString.DateTime.short(self.stats.start_datetime) if (
            self.stats.start_datetime) else EtaDefaults.low_data_string
        start_string = f"S: {start_string}"
        d.update(startS=start_string)
        startL_string = TimeString.DateTime.long(self.stats.start_datetime) if (
            self.stats.start_datetime) else EtaDefaults.low_data_string
        startL_string = f"S: {startL_string}"
        d.update(startL=startL_string)

        current_string = TimeString.DateTime.short(self.stats.current_datetime) if (
            self.stats.current_datetime) else EtaDefaults.low_data_string
        current_string = f"C: {current_string}"
        d.update(currentS=current_string)
        currentL_string = TimeString.DateTime.long(self.stats.current_datetime) if (
            self.stats.current_datetime) else EtaDefaults.low_data_string
        currentL_string = f"C: {currentL_string}"
        d.update(currentL=currentL_string)

        elapsed_string = TimeString.TimeDelta.short(self.stats.elapsed_timedelta) if (
            self.stats.elapsed_timedelta) else EtaDefaults.low_data_string
        elapsed_string = f"E: {elapsed_string}"
        d.update(elapsedS=elapsed_string)
        elapsedL_string = TimeString.TimeDelta.long(self.stats.elapsed_timedelta) if (
            self.stats.elapsed_timedelta) else EtaDefaults.low_data_string
        elapsedL_string = f"E: {elapsedL_string}"
        d.update(elapsedL=elapsedL_string)

        remaining_string = TimeString.TimeDelta.short(self.stats.remaining_timedelta) if (
            self.stats.remaining_timedelta) else EtaDefaults.low_data_string
        remaining_string = f"R: {remaining_string}"
        d.update(remainingS=remaining_string)
        remainingL_string = TimeString.TimeDelta.long(self.stats.remaining_timedelta) if (
            self.stats.remaining_timedelta) else EtaDefaults.low_data_string
        remainingL_string = f"R: {remainingL_string}"
        d.update(elapsedL=remainingL_string)

        eta_string = TimeString.DateTime.short(self.stats.eta_datetime) if (
            self.stats.eta_datetime) else EtaDefaults.low_data_string
        eta_string = f"ETA: {eta_string}"
        d.update(etaS=eta_string)
        etaL_string = TimeString.DateTime.long(self.stats.eta_datetime) if (
            self.stats.eta_datetime) else EtaDefaults.low_data_string
        etaL_string = f"ETA: {etaL_string}"
        d.update(etaL=etaL_string)

        return d
