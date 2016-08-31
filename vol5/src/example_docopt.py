"""docopt sample

Usage:
    example_docopt.py [-ab] <arg1> <arg2>
    example_docopt.py -h

Options:
    -a, --arg1  Argument1
    -b, --ball  Ball
"""
from docopt import docopt
if __name__ == "__main__":
	print(docopt(__doc__))
