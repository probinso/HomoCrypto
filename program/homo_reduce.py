#!/usr/bin/python


import sys

count=0
for i in sys.stdin:
    try:
        count+=int(i.strip())
    except:
        continue


print count
