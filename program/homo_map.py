#!/usr/bin/python
from circuits import *
from helpers import *
import sys
def main():
	count=0

	word="god"

	x=sys.stdin.readline().strip()

	x=int(x)
	query=[]
	for i in range(x):
		line=sys.stdin.readline().strip()
		query.append(int(line))
		

	
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
