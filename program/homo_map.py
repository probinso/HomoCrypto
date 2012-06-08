#!/usr/bin/python
from circuits import *
from helpers import *
import sys
def main():
	count=0

	word="God"
	wordbin = intListToBinList(word)
	for i in sys.stdin:
		try:
			line=[]
			for j in range(len(i)):
				try:
					line.append(int(i[j]))		
			
				except:
					continue
			count = search(wordbin,line,[0]) 
		except:
			#print "errorvaly on line",i
			continue
			
	print count

main()
