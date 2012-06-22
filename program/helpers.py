from fractions import Fraction
from math import ceil,log,copysign
from random import randrange
import sys 

def intToBinList(i):
    # turns integer into binary list representation
    return map(int,bin(i)[2:])


def binListToInt(l):
    # turns binary list into integer represenation
    return int(''.join(map(lambda x: str(int(x)),l)),2)


def roundFrac(f):
    # rounds fraction to nearest integer
    half = sign(int(f))*Fraction(1,2)
    return int(f + half)

def dotProduct(L1,L2):
    # returns dot product of two vectors
    assert(len(L1)==len(L2))
    return sum(map(lambda x: x[0]*x[1],zip(L1,L2)))

def sign(x):
    return cmp(x,0)

def bitLims(B):
    # returns the bit limits for a number of bits
    return (2**(B-1),(2**B)-1)


def randInt(B):
    # return int in bit range
    Min,Max = bitLims(abs(B))
    if B < 0: Min = -1*Max
    return randrange(Min,Max)


def mods(x,n):
   # this is our symmetric modulou
   a = x % n
   b = x % (-1*n)
   if abs(a)<abs(b): return a
   else: return b

def parityList(L):
    return map(lambda x : int(x%2), L)


def intListToBinList(string):
    """
    #takes a string and returns a list of binary representation of each letter
    newlist =[]
    word = list(string)
    fixed = makeFixedWidthConverter(8)
    for letter in word:
        newlist.append(fixed(intToBinList(ord(letter))))
    return reduce(lambda a,b: a+b,newlist)
    #return newlist
    """
    # takes in a string returns list of bits
    fixed = makeFixedWidthConverter(8)
    return sum(map(lambda x: 
                   fixed(map(int,bin(ord(x))[2:])),
                   string)
               )

def split(input,size):
    # splits list into a list of lists each length size
    return [input[start:start+size] for start in range(0,len(input),size)]

def wordBinListToString(l):
    #takes a list of binary representations of letters and returns a string
    word =""
    for letter in split(l,8):
        word += chr(binListToInt(letter))
    return word


def makeFixedWidthConverter(D):
    # takes in a fixed width and produces 
    # a function that takes a binary represenation
    # of an integer, to a fixed width equivelent
    def toFixedWidth(L):
        # we assume that the input comes in with 
        # a leading bit denoting the sign
        if len(L) == D:
            return L
        store = [0]*D    # this does not preserve sign
        #store = [L[0]]*D # this preserves sign
        store[-1*len(L):] = L[::]
        return store
    return toFixedWidth

