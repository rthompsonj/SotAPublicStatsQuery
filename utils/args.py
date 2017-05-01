import argparse

class Argument(object):
    def __init__(self, short_arg, long_arg, default_value, help_text):
        self.short = short_arg
        self.long = long_arg
        self.help = '{} (default: "{}")'.format(help_text, default_value)
        self.default = default_value

ARGS = [
    Argument('-o', '--output', 'output.json', 'Output file name'),
    Argument('-st', '--search-term', '*', 'Search term'),
    Argument('-tf', '--time-frame', 0.04, 'Time frame in days'),
]

def get_args():
    parser = argparse.ArgumentParser()
    for arg in ARGS:
        parser.add_argument(arg.short, arg.long,
                            type=type(arg.default),
                            help=arg.help,
                            default=arg.default)
    return parser.parse_args()
