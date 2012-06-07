#!/usr/bin/python


import sys
from circuits import *
from helpers import *


def main():

	wordbin = ''

	for i in sys.stdin:
		wordbin += i[:-1]
		wordbin += ' '
	
	wordbin = intListToBinList(wordbin)

	print str(wordbin)[1:-1]
		
		
main()
