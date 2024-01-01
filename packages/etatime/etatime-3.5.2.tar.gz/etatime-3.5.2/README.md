# ETA Time
### A library for tracking, computing, and formatting time estimates in Python. (Based on `tqdm`.)
[![Python Version](https://img.shields.io/pypi/pyversions/etatime?logo=python&logoColor=white)](https://pypi.org/project/etatime/)
[![PyPI Version](https://img.shields.io/pypi/v/etatime?logo=PyPI&logoColor=white)](https://pypi.org/project/etatime/)

[![GitHub Build](https://img.shields.io/github/actions/workflow/status/nimaid/python-etatime/master.yml?logo=GitHub)](https://github.com/nimaid/python-etatime/actions/workflows/master.yml)
[![Coveralls Coverage](https://img.shields.io/coverallsCoverage/github/nimaid/python-etatime?logo=coveralls)](https://coveralls.io/github/nimaid/python-etatime)
[![Codecov Coverage](https://img.shields.io/codecov/c/github/nimaid/python-etatime?logo=codecov&logoColor=white)](https://codecov.io/gh/nimaid/python-etatime)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3623bf84675842359f12d73682023429)](https://app.codacy.com/gh/nimaid/python-etatime/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

[![License](https://img.shields.io/pypi/l/etatime?logo=opensourceinitiative&logoColor=white)](https://github.com/nimaid/python-etatime/raw/main/LICENSE)
[![PyPI Downloads](https://img.shields.io/pypi/dm/etatime.svg?label=pypi%20downloads&logo=PyPI&logoColor=white)](https://pypi.org/project/etatime/)



## Why?
[tqdm](https://github.com/tqdm/tqdm) is probably the most popular option for Python programmers to show progress in their programs. However, I wasn't happy with the default formatting code options, and wanted something that was easier to read and understand for an average user.

In addition, I wanted to be able to access information like ETA in my code. While `tqdm` sort of lets you do this, it's not well documented, and you would have to dig through the source code to get the values and formulas you want.

`etatime` is my answer to this. It's a minimal wrapper around `tqdm` that adds additional formatting codes and well-documented progress stats tracking.

## Basic Usage
The main feature of this library is the `EtaBar` class. This is a wrapper for the `tqdm.tqdm` class that provides variables which track important ETA state information for use elsewhere in your code.

This uses another package I made called `timefmt` to format the times into human-readable text.

*For more information on the `:=` (walrus) operator, see [the documentation.](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions)*

```python
import time, random
import timefmt
from etatime import EtaBar

for item in (eta := EtaBar(range(9999999))):  # Creates a progress bar which tracks stats
    ...  # Do your processing here

print(f"Done processing {eta.stats.total_items} items in {timefmt.td.long(eta.stats.elapsed_timedelta)}!\n")
```
Here is an example of the sort of output this produces:
```
 14%|█▍        | 1432400/9999999 | R: 0:00:02 | ETA: 5:22:13 PM
 ...
100%|██████████| 9999999/9999999 | R: ??? | ETA: ???
Done processing 9999999 items in 2 seconds!
```

You can get more verbose information by replacing the for loop with this:
```python
from etatime import EtaBar

for item in (eta := EtaBar(range(9999999), bar_format="{l_bar}{bar}{r_barL}")):
    ...  # Do your processing here
```
Here is an example of the long output:
```
 35%|███▌      | 3545009/9999999 | R: 1 second | ETA: 5:26:11 PM MST
```

All keyword arguments other than `bar_format` get passed directly to `tqdm.tqdm`. `bar_format` is pre-processed by `etatime` in order to inject some new custom [formatting codes](https://tqdm.github.io/docs/tqdm/#tqdm-objects):
* `startS`: The starting time in short digit format.
* `startL`: The starting time written out in plain english.
* `currentS`: The current (loop start time) time in short digit format.
* `currentL`: The current (loop start time) time written out in plain english.
* `elapsedS`: The elapsed time in short digit format.
* `elapsedL`: The elapsed time written out in plain english.
* `remainingS`: The remaining time in short digit format.
* `remainingL`: The remaining time written out in plain english.
* `etaS`: The ETA time in short digit format.
* `etaL`: The ETA time written out in plain english.
* `r_barS` == `"| {n_fmt}/{total_fmt} | {remainingS} | {etaS}"`
* `r_barL` == `"| {n_fmt}/{total_fmt} | {remainingL} | {etaL}"`

The following attributes are available in the `stats` data class of the `EtaBar` instance:
* `total_items`
* `rate`
* `initial`
* `n`
* `percent`
* `start_time` (seconds)
  * `start_datetime`
* `current_time` (seconds)
  * `current_datetime`
* `elapsed_time` (seconds)
  * `elapsed_timedelta`
* `remaining_time` (seconds)
  * `remaining_timedelta`
* `eta_time` (seconds)
  * `eta_datetime`

# Full Documentation
<p align="center"><a href="https://etatime.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="etautil on Read the Docs"></a></p>
