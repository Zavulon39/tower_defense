class ConsoleColor:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class RainbowPrint:

    @staticmethod
    def print(color, *args, sep=' ', end='\n', file=None):
        print(color, *args, ConsoleColor.END, sep=sep, end=end, file=file)
