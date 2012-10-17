import math
import random

from random import randint
from random import choice

from helpers import *

##Changelog Bitlims was returning bit shifts instead of powers.


## Initialization Tools ##

def getNPQ(N):
    # N is a security parameter
    P = N**2
    Q = N**3
    return (N,P,Q)

def genKey(P):
    kn,kx = bitLims(P)
    k = randint(kn,kx)
    k = k-((k%2)-1)
    return k

def decrypt(L,p):
    return map(lambda x: mods(x,p) % 2,L)


def makeEncrypt(N,Q):
    def makeEncryptBit(N,Q):
        Mn,Mx = bitLims(N)
        Qn,Qx = bitLims(Q)
        return lambda m,p: randint(Qn,Qx)*p + 2*(randint(Mn,Mx)//2) + m

    F = makeEncryptBit(N,Q)
    return (lambda L,p : [F(x,p) for x in L])

"""
#Helper Binary Array and Integer Functions
def a2b(a):
    ai = ord(a)
    return ''.join('01'[(ai >> x) & 1] for x in xrange(7, -1, -1))


def strBin(s):
    def a2b(a):
        ai = ord(a)
        return ''.join('01'[(ai >> x) & 1] for x in xrange(7, -1, -1))

    def split_len(seq):
        def convert(c):
            if c == '0': return 0
            else: return 1

        return [convert(seq[i:i+1]) for i in range(0, len(seq), 1)]

    return reduce(lambda a,b: a+b,map(lambda x: split_len(a2b(x)),s))
"""

def testSearch(Secure,S1,S2):
    N,P,Q = getNPQ(Secure)
    encrypt = makeEncrypt(N,Q)

    K = genKey(P)
    K2= K
    bit1 = strBin(S1)
    bit2 = strBin(S2)
    enc1,enc2 = encrypt(bit1,K),encrypt(bit2,K)
    acc = encrypt([0]*(len(enc2)//8),K)
    zero = acc[:]
    encs = search(enc1,enc2,acc,zero)
    print " ",decrypt(encs,K)


Security_Param = 64
S1 = "a"
S2 = "c aa "

#testSearch(Security_Param,S1,S2)

## AsymKeyGen


def fheKeyGen(S):
    private, public, encrypt = asymKeyGen(S)
    Alpha, Beta = int(math.sqrt(S)), S
    x = 1.0/private

    SparseSubset = []
    Hint = []
    S = []

    for i in range(Alpha-1):
        SparseSubset.append(random.random()*x)
        x = x - SparseSubset[-1]
    SparseSubset.append(x)

    for i in range(Beta-Alpha):
        Hint.append(random.random()*2)

    for i in SparseSubset:
        index=randint(0,len(Hint))
        Hint.insert(index,i)

    for i in SparseSubset:
        S.append(Hint.index(i))

    return (public,Hint),(private,S),encrypt

