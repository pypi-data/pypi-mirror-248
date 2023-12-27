import math

from etatime.constants import EtaDefaults, CompletionDefaults


def progress_char(value):
    char = "█"
    if value < 1 / 8:
        char = " "
    elif value < 2 / 8:
        char = "▏"
    elif value < 3 / 8:
        char = "▍"
    elif value < 4 / 8:
        char = "▌"
    elif value < 5 / 8:
        char = "▋"
    elif value < 6 / 8:
        char = "▊"
    elif value < 7 / 8:
        char = "▉"

    return char


class Completion:
    def __init__(
            self,
            total,
            index
    ):
        self.total = total
        self.index = index

    def value(self):
        return self.index / self.total

    def string(
            self,
            decimals=EtaDefaults.percent_completion,
            verbose=EtaDefaults.verbose
    ) -> str:
        percent = self.value()
        percent_format = f"{{:.{decimals}f}}%"

        result = percent_format.format(percent * 100)
        if verbose:
            result += f" ({self.index}/{self.total})"

        return result

    def bar(
            self,
            width=CompletionDefaults.width
    ):
        value = self.value()
        complete_chars = math.floor(width * value)

        bar_string = ""
        for char in range(width):
            if char < complete_chars:
                bar_string += progress_char(1)
            elif char > complete_chars:
                bar_string += progress_char(0)
            else:
                bar_string += progress_char((value * width) % 1)

        return bar_string
