#!/usr/bin/env python

import elv
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: test.py file.csv")
    else:
        trans = elv.parse(sys.argv[1])
        print(repr(trans))
