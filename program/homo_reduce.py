#!/usr/bin/python

from circuits import *
import sys

def main():
	count = [0]
	for i in sys.stdin:
		try:
			i = map(int, i[2:-2].split(","))
			count = Add16(count,i)
		except:
			print i
			continue
<<<<<<< HEAD

	print count
=======
	sys.stdout.write(str(count))
>>>>>>> 1c6b566b555e6abfe6b76aed9e37744080a73a84
main()
