# ETA Time
### A library for tracking, computing, and formatting time estimates in Python.

## Basic Usage
For more information on the `:=` (walrus) operator, see [the documentation.](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions)
```python
import time, random
from etatime.eta import eta_calculator


# Just a placeholder function that takes a random amount of time
def process_item(item):
    time.sleep(random.random() * 20)


for item in (calc := eta_calculator(range(10))):  # Creates a `calc` object that tracks the progress
    print(calc.eta)  # Print the current progress stats
    process_item(item)  # Do your processing here

print(f"Done processing {calc.eta.total_items} items in {calc.eta.string(calc.eta.Value.TIME_TAKEN)}!\n")
```
Here is an example of the sort of output this produces:
```
0.00%
10.00% | R: 0:01:33 | E: 12:25:16 AM
20.00% | R: 0:01:56 | E: 12:25:57 AM
30.00% | R: 0:01:13 | E: 12:25:16 AM
40.00% | R: 0:00:55 | E: 12:25:03 AM
50.00% | R: 0:00:55 | E: 12:25:22 AM
60.00% | R: 0:00:43 | E: 12:25:18 AM
70.00% | R: 0:00:32 | E: 12:25:19 AM
80.00% | R: 0:00:19 | E: 12:25:09 AM
90.00% | R: 0:00:09 | E: 12:25:00 AM
Done processing 10 items in 0:01:33!
```

You can get more verbose information by replacing the for loop with this:
```python
for item in (calc := eta_calculator(range(10), verbose=True)):
```
Here is an example of the verbose output:
```
0.00% (0/10)
10.00% (1/10) | Time remaining: 1 minute and 54 seconds | ETA: 12:27:33 AM US Mountain Standard Time
20.00% (2/10) | Time remaining: 1 minute and 33 seconds | ETA: 12:27:22 AM US Mountain Standard Time
30.00% (3/10) | Time remaining: 1 minute and 7 seconds | ETA: 12:27:02 AM US Mountain Standard Time
40.00% (4/10) | Time remaining: 50 seconds | ETA: 12:26:49 AM US Mountain Standard Time
50.00% (5/10) | Time remaining: 51 seconds | ETA: 12:27:08 AM US Mountain Standard Time
60.00% (6/10) | Time remaining: 41 seconds | ETA: 12:27:09 AM US Mountain Standard Time
70.00% (7/10) | Time remaining: 28 seconds | ETA: 12:27:01 AM US Mountain Standard Time
80.00% (8/10) | Time remaining: 20 seconds | ETA: 12:27:05 AM US Mountain Standard Time
90.00% (9/10) | Time remaining: 10 seconds | ETA: 12:27:07 AM US Mountain Standard Time
Done processing 10 items in 1 minute and 51 seconds!
```

You can also build a custom message piece-by-piece, like so:
```python
print(f"Processing item: '{item}'")
print(f"  Completed: {calc.eta.string(calc.eta.Value.COMPLETION)}")
print(f"  Time taken: {calc.eta.string(calc.eta.Value.TIME_TAKEN)}")
print(f"  Time remaining: {calc.eta.string(calc.eta.Value.TIME_REMAINING)}")
print(f"  ETA: {calc.eta.string(calc.eta.Value.ETA)}")
```
This produces the following output:
```
Processing item: '0'
  Completed: 0.00% (0/10)
  Time taken: 0 seconds
  Time remaining: not enough data
  ETA: not enough data
Processing item: '1'
  Completed: 10.00% (1/10)
  Time taken: 11 seconds
  Time remaining: 1 minute and 38 seconds
  ETA: 12:29:31 AM US Mountain Standard Time
Processing item: '2'
  Completed: 20.00% (2/10)
  Time taken: 29 seconds
  Time remaining: 1 minute and 55 seconds
  ETA: 12:30:05 AM US Mountain Standard Time
Processing item: '3'
  Completed: 30.00% (3/10)
  Time taken: 47 seconds
  Time remaining: 1 minute and 50 seconds
  ETA: 12:30:18 AM US Mountain Standard Time
Processing item: '4'
  Completed: 40.00% (4/10)
  Time taken: 54 seconds
  Time remaining: 1 minute and 21 seconds
  ETA: 12:29:57 AM US Mountain Standard Time
Processing item: '5'
  Completed: 50.00% (5/10)
  Time taken: 56 seconds
  Time remaining: 56 seconds
  ETA: 12:29:33 AM US Mountain Standard Time
Processing item: '6'
  Completed: 60.00% (6/10)
  Time taken: 1 minute and 3 seconds
  Time remaining: 42 seconds
  ETA: 12:29:27 AM US Mountain Standard Time
Processing item: '7'
  Completed: 70.00% (7/10)
  Time taken: 1 minute and 22 seconds
  Time remaining: 35 seconds
  ETA: 12:29:38 AM US Mountain Standard Time
Processing item: '8'
  Completed: 80.00% (8/10)
  Time taken: 1 minute and 28 seconds
  Time remaining: 22 seconds
  ETA: 12:29:32 AM US Mountain Standard Time
Processing item: '9'
  Completed: 90.00% (9/10)
  Time taken: 1 minute and 48 seconds
  Time remaining: 12 seconds
  ETA: 12:29:41 AM US Mountain Standard Time
Done processing 10 items in 1 minute and 57 seconds!
```

You can also make a progress bar similar to how you would with tqdm:
```python
import sys
import time, random
from etatime.eta import eta_bar


# Just a placeholder function that takes a random amount of time
def process_item(item):
    time.sleep(random.random() * 20)


for item in (pbar := eta_bar(range(10), verbose=True, width=12, file=sys.stdout)):  # Updates the progress bar each loop
    process_item(item)  # Do your processing here

print(f"Done processing {pbar.eta.total_items} items in {pbar.eta.string(pbar.eta.Value.TIME_TAKEN)}!\n")
```
Which gives the following output (on a single line):
```
|            | 0.00% (0/10)
|█▏          | 10.00% (1/10) | Time remaining: 2 minutes and 50 seconds | ETA: 9:48:42 PM US Mountain Standard Time
|██▌         | 20.00% (2/10) | Time remaining: 1 minute and 48 seconds | ETA: 9:47:48 PM US Mountain Standard Time
|███▋        | 30.00% (3/10) | Time remaining: 1 minute and 44 seconds | ETA: 9:48:02 PM US Mountain Standard Time
|████▉       | 40.00% (4/10) | Time remaining: 1 minute and 27 seconds | ETA: 9:47:58 PM US Mountain Standard Time
|██████      | 50.00% (5/10) | Time remaining: 1 minute and 14 seconds | ETA: 9:48:02 PM US Mountain Standard Time
|███████▏    | 60.00% (6/10) | Time remaining: 1 minute and 2 seconds | ETA: 9:48:08 PM US Mountain Standard Time
|████████▌   | 70.00% (7/10) | Time remaining: 45 seconds | ETA: 9:48:04 PM US Mountain Standard Time                                                               
|█████████▋  | 80.00% (8/10) | Time remaining: 29 seconds | ETA: 9:48:01 PM US Mountain Standard Time
|██████████▉ | 90.00% (9/10) | Time remaining: 13 seconds | ETA: 9:47:50 PM US Mountain Standard Time
|████████████| 100.00% (10/10) | Time taken: 2 minutes and 16 seconds | Completion time: 9:45:32 PM US Mountain Standard Time
```
You can even access eta variables inside the for loop:
```python
for item in (pbar := eta_bar(range(10), verbose=False)):  # This makes a new non-verbose progress bar
    long_progress_string = pbar.eta.progress_string(verbose=True)  # Use the eta variables elsewhere
    process_item(item)
    ...
```

# Full Documentation
<p align="center"><a href="https://etatime.readthedocs.io/en/latest/index.html"><img src="https://brand-guidelines.readthedocs.org/_images/logo-wordmark-vertical-dark.png" width="300px" alt="etautil on Read the Docs"></a></p>
