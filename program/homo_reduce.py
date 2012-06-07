#!/usr/bin/python

from circuits import *
import sys

count = [0]
for i in sys.stdin:
	i = map(int, i[1:-2].split(","))
	count = Add16(count,i)


print count
