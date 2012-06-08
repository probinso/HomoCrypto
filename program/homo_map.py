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
<<<<<<< HEAD
			break
		except ValueError:
			x=open("/hdfs/tmp/error.txt","a")
			x.write("value error on input:"+i)
			x.close()
	print str(count)
=======
		except:
			#print "errorvaly on line",i
			continue
			
	print count
>>>>>>> 1c6b566b555e6abfe6b76aed9e37744080a73a84

main()
