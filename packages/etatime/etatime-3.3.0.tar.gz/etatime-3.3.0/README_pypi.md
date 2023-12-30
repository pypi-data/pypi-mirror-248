# ETA Time
### A library for tracking, computing, and formatting time estimates. (Based on `tqdm`.)

## Why?
[tqdm](https://github.com/tqdm/tqdm) is probably the most popular option for Python programmers to show progress in their programs. However, I wasn't happy with the default formatting code options, and wanted something that was easier to read and understand for an average user.

In addition, I wanted to be able to access information like ETA in my code. While `tqdm` sort of lets you do this, it's not well documented, and you would have to dig through the source code to get the values and formulas you want.

`etatime` is my answer to this. It's a minimal wrapper around `tqdm` that adds additional formatting codes and well-documented progress stats tracking.

*The `time` submodule is pretty useful too.*

## Basic Usage
The main feature of this library is the `EtaBar` class. This is a wrapper for the `tqdm.tqdm` class that provides variables which track important ETA state information for use elsewhere in your code.

Additionally, the `TimeString` class provides methods to format the resultant time objects into human-readable text. This is used inside `EtaBar` class to add additional `bar_format` codes.

*For more information on the `:=` (walrus) operator, see [the documentation.](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions)*

```python
import time, random
from etatime import EtaBar, TimeString


# Just a placeholder function that takes a random amount of time
def process_item(item):
    time.sleep(random.random())


for item in (eta := EtaBar(range(100))):  # Creates a progress bar which tracks stats
    process_item(item)  # Do your processing here

print(f"Done processing {eta.Stats.total_items} items in {TimeString.automatic(eta.Stats.elapsed_timedelta, long=True)}!\n")
```
Here is an example of the sort of output this produces:
```
 16%|█▌        | (16/100) | R: 0:00:17 | ETA: 3:13:26 AM
 ...
 100%|██████████| (100/100) | R: 0:00:01 | ETA: 3:46:01 AM
Done processing 100 items in 53 seconds!
```

You can get more verbose information by replacing the for loop with this:
```python
for item in (eta := EtaBar(range(100), bar_format="{l_bar}{bar}| {remainingL} | {etaL}")):
```
Here is an example of the long output:
```
 13%|█▎        | (13/100) | Remaining: 20 seconds | ETA: 3:12:16 AM US Mountain Standard Time
```

All keyword arguments other than `bar_format` get passed directly to `tqdm.tqdm`. `bar_format` is pre-processed by `etatime` in order to inject some new custom [formatting codes](https://tqdm.github.io/docs/tqdm/#tqdm-objects):
- `startS`: The starting time in short digit format.
- `startL`: The starting time written out in plain english.
- `currentS`: The current (loop start time) time in short digit format.
- `currentL`: The current (loop start time) time written out in plain english.
- `elapsedS`: The elapsed time in short digit format.
- `elapsedL`: The elapsed time written out in plain english.
- `remainingS`: The remaining time in short digit format.
- `remainingL`: The remaining time written out in plain english.
- `etaS`: The ETA time in short digit format.
- `etaL`: The ETA time written out in plain english.

The following attributes are available in the `Stats` class of the `EtaBar` instance:
- `total_items`
- `rate`
- `initial`
- `n`
- `percent`
- `start_time` (seconds)
  - `start_datetime`
- `current_time` (seconds)
  - `current_datetime`
- `elapsed_time` (seconds)
  - `elapsed_timedelta`
- `remaining_time` (seconds)
  - `remaining_timedelta`
- `eta_time` (seconds)
  - `eta_datetime`

# Full Documentation
<p align="center"><a href="https://etatime.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="etautil on Read the Docs"></a></p>
