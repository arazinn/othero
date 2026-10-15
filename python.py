#!/usr/bin/python3
import sys


def tonum(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


x = 0
for line in sys.stdin:
    x += tonum(line)

print(x)
