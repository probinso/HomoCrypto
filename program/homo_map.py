#!/usr/bin/python
from circuits import *
from helpers import *
import sys
def main():
	count=0

	word="god"
	wordbin = intListToBinList(word)
	start=True
	for i in sys.stdin:
		line = map(int,i[:-1])		
		count += binListToInt(parityList(search(wordbin,intListToBinList("god god god hi hi"),[0],[0])))
	print count

main()
