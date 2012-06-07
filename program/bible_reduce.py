#!/usr/bin/python

from circuits import *
import sys

for i in sys.stdin:
	i = i.split(", ")

	#biblebit = file("/tmp/biblebit.txt","a")
	for x in i:
		#biblebit.write(str(x))
		sys.stdout.write(str(x))
	#biblebit.close()
	
