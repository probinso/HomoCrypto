from random import randint
from random import random
from random import choice
import math

##Changelog Bitlims was returning bit shifts instead of powers.


def mods(x,n):
   # this is our symmetric modulou
   a = x % n
   b = x % (-1*n)
   if abs(a)<abs(b): return a
   else: return b


## Initialization Tools ##

def getNPQ(N):
    # N is a security parameter
    P = N**2
    Q = N**5
    return (N,P,Q)


def bitLims(B):
    return (2**(B-1),(2**B)-1)

def genKey(P):
   kn,kx = bitLims(P)
   k = randint(kn,kx)
   #print "k b4"
   #print k
   k = k-((k%2)-1)
   return k

def decrypt(L,p):
    return map(lambda x: mods(x,p) % 2,L)

def makeEncrypt(N,Q):
   def makeEncryptBit(N,Q):
      Mn,Mx = bitLims(N)
      Qn,Qx = bitLims(Q)
      return lambda m,p: randint(Qn,Qx)*p + 2*(mods(randint(Mn,Mx),p)//2) + m
   
   F = makeEncryptBit(N,Q)
   return (lambda L,p : [F(x,p) for x in L])
   
   


#Helper Binary Array and Integer Functions

## Bit Operations ##
def bxor(a,b):
    return a+b

def bnot(a):
    return 1-a

def band(a,b):
    return a*b

def bnand(a,b):
    return bnot(band(a,b))

def bor(a,b):
    return bnand(bnand(a,a),bnand(b,b))

## Bit List Ops ##
def myxor(L1,L2):
   return map(lambda x: bxor(x[0],x[1]),zip(L1,L2))

def myand(L1,L2):
   return map(lambda x: band(x[0],x[1]),zip(L1,L2))

def mynot(L1):
   # This surprisingly works.
   return map(lambda x: bnot(x),L1)


## Complex Operators ##
def myadd(L1,L2):
   def carry(A,B,C):
      # This is the carry logic that clark
      # provided for the adder
      return A*B+A*C+B*C
   
   # apparently reverse() is an in-place
   # side-effects driven procedure
   #
   # also the carry bit gets way out of
   # controle. There should be a moduluo
   # however I have not gotten to that.
   Z = zip(L1,L2)
   Z.reverse()
   # the reverse is needed to preserve the
   # endian of this data.
   C = [0]
      
   for x in Z:
      C = [carry(x[0],x[1],C[0])] + C
   
   # print decrypt(C,11)
   C = zip([0]+L1,[0]+L2,C)
   return map(lambda x: x[0]+x[1]+x[2],C)



def search(L1,L2,acc,Zeros):
    
    if len(L2)<len(L1):
        return acc
    
    List = myxor(L1,L2)
    Zeros[-1]= bnot(reduce(lambda x,y: bor(x,y),List))
    acc = myadd(acc,Zeros)[1:]
    
    return search(L1,L2[8:],acc,Zeros)


## Userland Helper Operations ##

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
        SparseSubset.append(random()*x)
        x = x - SparseSubset[-1]
    SparseSubset.append(x)
    
    for i in range(Beta-Alpha):
        Hint.append(random()*2)
    
    for i in SparseSubset:
        index=randint(0,len(Hint))
        Hint.insert(index,i)
        
    for i in SparseSubset:
        S.append(Hint.index(i))
    
    return (public,Hint),(private,S),encrypt


"""
def randomSubsetSum (pKeyList):
s=0
lp=random.randint(1,len(pkeyList))
for i in range(lp):
s+=pKeyList(i)
return s

def asymEncrypt(P,Q):
#Use AsymKeyGen to make a private key and a secret key list
#choose random elements from public key list and sum them
#If this sum mod sk is stll

"""
