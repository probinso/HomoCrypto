#!/usr/bin/python
from circuits import *
from helpers import *
import sys
def main():
	count=0

	word="God"
	wordbin = intListToBinList(word)
	for i in sys.stdin:
		line = map(int,i[:-1])		
		count = search(wordbin,line,[0]) 
	print count

main()
