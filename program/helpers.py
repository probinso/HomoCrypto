from fractions import Fraction
from math import ceil,log
from random import randrange


def intToBinList(i):
    # turns integer into binary list representation
    return map(int,bin(i)[2:])


def binListToInt(l):
    # turns binary list into integer represenation
    return int(''.join(map(lambda x: str(int(x)),l)),2)


def roundFrac(f):
    # rounds fraction to nearest integer
    y = int(f)
    if f - y >= Fraction(1,2): y +=1 
    return y


def dotProduct(L1,L2):
    # returns dot product of two vectors
    assert(len(L1)==len(L2))
    return sum(map(lambda x: x[0]*x[1],zip(L1,L2)))


def bitLims(B):
    # returns the bit limits for a number of bits
    return (2**(B-1),(2**B)-1)


def randInt(B):
    # return int in bit range
    Min,Max = bitLims(abs(B))
    if B < 0: Min *= -1
    return randrange(Min,Max)


def mods(x,n):
   # this is our symmetric modulou
   a = x % n
   b = x % (-1*n)
   if abs(a)<abs(b): return a
   else: return b


def parityList(L):
    return map(lambda x : int(x%2), L)


def intListToBinList(i):
    #takes a string and returns a list of binary representation of each letter
    newlist =[]
    word = list(i)
    for letter in word:
        newlist.append(intToBinList(ord(letter)))
    return newlist


def wordBinListToString(l):
    #takes a list of binary representations of letters and returns a string
    word =""
    for letter in l:
        word += chr(binListToInt(letter))
    return word


def makeFixedWidthConverter(D):
    # takes in a fixed width and produces 
    # a function that takes a binary represenation
    # of an integer, to a fixed width equivelent
    def toFixedWidth(L):
        # we assume that the input comes in with 
        # a leading bit denoting the sign
        assert(len(L) <= D)
        if len(L) == D:
            return L
        store = [0]*D    # this does not preserve sign
        #store = [L[0]]*D # this preserves sign
        store[-1*len(L):] = L[::]
        return store
    return toFixedWidth

