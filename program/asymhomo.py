import random

from itertools import izip,islice
from math import ceil,log
from fractions import Fraction

from homo import *
from helpers import *

from circuits import *

debug=True

#Asym PHE Helper Functions
def privateKeyGen(P):
    return genKey(P)


def distribute(sk,N,Q):
    #q=random.randrange(0,(2**((N**5)))//sk)
    """
      do not know why dividing by sk for the code above .
    """
    q = randInt(N**5)
    r = randInt(-1*N)
    return sk*q+r


def publicKeyGen(sk,N):
    N,P,Q=getNPQ(N)
    pk=[]
    for i in range(Q+N):
        pk.append(distribute(sk,N,Q))
    maximal=max(pk)
    maxindex=pk.remove(maximal)
    pk.insert(0,maximal)
    if maximal%2==0 or mods(maximal,sk)%2!=0:
        pk=publicKeyGen(sk,N)
    return pk


def randomSubSetSum(pk):
    #Defaults to 2 rite now get over it
    return sum([choice(pk[1:]) for i in range(10)])

def asymKeyGen(N):
    N,P,Q=getNPQ(N)
    sk=privateKeyGen(P)
    pk=publicKeyGen(sk,N)
    return (sk,pk)


#message is an array pk is a public key array
def encrypt(message,pk,N):
    """
    The code above is not secure. It is likely that randomSubSetSum(pk)
    will introduce a constant of too much noise and because these values
    do not reset, on a per-loop basis you are likely to produce a negation
    to every bit by forcing overflow. That is why we were getting bad answers
    we were recieving 3 times the noise for every bit

    Okay now I understand, and I have updated randomSubSetSum to return
    a summation over 10 keys. Now we are getting 'more' conistant results.
    What needed to happen was updating the traditional
    """

    _,mx = bitLims(2*N)

    cipher = [(2*(randomSubSetSum(pk)+(random.randrange(-1*mx,mx)))+i)% pk[0] for i in message]

    #print "encrypted bits :: ",[x % 2 for x in cipher]
    return cipher


def decrypt(cipher,sk):
    message = [int(mods(i,sk)%2) for i in cipher]
    return message


#TODO code correct a/b values
def getAlphaBeta(N):
    """
      this is supposed to produce alpha,beta tupple
      such that
        beta \approx (lambda^5)
        (beta choose alpha) \approx (beta ^ alpha)
      these are parameters used for generating our
      subset-sum problem. our Set will be length Beta,
      our subset-sum solution will be length alpha

      I do not know how to do this.
      --------------------------------------------

      we adopt a new definition!

      \alpha = \lambda
                    _                                           _
                   | ((\lambda^2)(\lambda^5))                    | ^ 6
      \beta\approx | ------------------------ * (log_2(\lambda)) |
                   |      (2 * \lambda)                          |
                   --                                          --
      as sited on page 15 of Fully Homomorphic Encryption
        Over the Integers;  June 8th 2010
        Dijk,Gentry,Halevi,Vaikuntanathan
    """
    return (N,N**2)#(N,N**5) #int(((((N**6)+1)//2)*log(N,2))**6))


#Generates key pairs and hints
def fheKeyGen(N):
    """
      This is the fully homomorphic encryption scheme key
      generator. Takes in Security Parameter
    """
    N,P,Q=getNPQ(N)
    alpha,beta=getAlphaBeta(N)
    sk=privateKeyGen(P)
    pk=publicKeyGen(sk,N)

    hint=hintGen(Fraction(1,sk),alpha)
    garbage=garbageGen(beta,alpha)
    y,S=hide(hint,garbage)
    # y holds list of quotients
    # S holds list of indexes

    return ((sk,S),(pk,y))


#Notes about limiting Hints:
#Limit the precsion of the hint rationals to Lg Alpha +3
def hintGen(f,alpha):
    """
    This takes in a floating point number representative of
    1/secret_key, and alpha denoting the size of the subset
    for our subset-sum problem

    produces the subset-sum that will be indexed into later
    """

    F = lambda x: Fraction(round(
            random.random(),     # produce random number \in (0,1)
            int(log(alpha,2)+3+1)# to this many degrees of accuracy
            ))*x# then cast it as a Fraction
    """
    we move *x to the outside of the function above because we
    want to insure that the function does not round to zero
    before the round function can be applied.

    Additional Note about security. This produces a list of
    likely decreasing values. Although they will be randomly
    placed throughout our final list, knowing this may result
    in comprimised security. Further investigation needed.
    """

    SparseSubset = []

    for i in range(alpha-1):
        x = F(f)
        SparseSubset.append(x)
        f = f - x

    SparseSubset.append(f)

    return SparseSubset


def garbageGen(beta,alpha):
    """
    This produces the garbage bits that produce the coset for
    the subset-sum problem (length beta-alpha)
    """

    garbage=[]
    for i in xrange(beta-alpha):
        garbage.append(
            Fraction(
                round(
                    random.random()*2,
                    int(ceil(log(alpha,2)+3))
                    )
                )
            )
        

    return garbage


def random_insert_seq(lst, seq):
    insert_locations = sample(xrange(len(lst) + len(seq)), len(seq))
    inserts = dict(zip(insert_locations, seq))
    input = iter(lst)
    lst[:] = [
        inserts[pos] if pos in inserts else next(input)
        for pos in xrange(len(lst) + len(seq))
        ]
    return lst


def hide(hint,garbage):
    """
    Takes in Hint and Garbage cosets to produce a random
    ordering to their combination.
    """

    for h in hint:
        index=random.randrange(0,len(garbage)-1)
        garbage.insert(index,h)

    S = [garbage.index(h) for h in hint]
    
    return (garbage,S)


def fheEncrypt(message,pk,y,N):
    """
    Fhe Encrypt message is array pk is the set, y is the hidden sk,
    N is the security parameter

    pk = one of the public keys
    y  = the set of values for subset-sum security
    N  = security parameter
    """

    c = encrypt(message,pk,N)
    cipher = [(x,multCipherHint(x,y)) for x in c]

    return cipher


#bultiplies a encuphered text by the hint
def multCipherHint(encbit,y):
    ctotup = [(encbit* x)%2 for x in y]
    return ctotup


#This needs Roundingz
def fheDecrypt(cy,S):
    """
    tupples?
    """

    message=[((x[0]%2)+(hintsum(x[1],S) %2))%2 for x in cy]

    return message


#This is doing the summing the wrong values
def hintsum(y,S):

    val = roundFrac(sum([y[i] for i in S]))
    return val


def encryptSk(sk,pk,N):
    """
    Used to Ecnrypt the Secret Key List with a new public Key
    """

    #the Sk list is a bunch of indecies. In order to do a recrypt it would need to be
    #A Vector of 1's and zeros as Gentry Described. This function uses the public key to encrypt the secret key
    #and returns encS. Client would need to make this and send it to the server
    _, beta = getAlphaBeta(N)
    encS=[0]*(beta)

    for i in sk:
        encS[i]=1

    print "ready to encrypt S"
    return encrypt(encS,pk,N)


def fheExpandBit(c,y):
    # cy denotes exclusively the twiddled ciphertext
    # pk denotes the public encryption key set
    # y denotes our subsetsum vector
    # N is aparently for fun ...

    return [ roundFrac(c*yi)%2 for yi in y ]


def fheRecrypt(cy,pk,y,encS,N):
    """
    FHE Recrypt works as follows:
    """
    pass


#FHE Encrypt with Given pk rather than rss p
def doubleEncrypt(cipher,pk,y,N):
    c=encrypt(cipher,pk,N)
    cipher=[]
    for i in range(len(c)):
        cipher.append((c[i],multCipherHint(c[i],y)))
    return cipher


#For Each Y in CY dot product Y,encS and return lsb(c) xor lsb(product)
def doubleDecrypt(cy,encS):
    message=[]
    for i in cy:
        c=i[0]
        y=i[1]
        message.append(abs( mods((mods(c,2) + mods(dotProduct(y,encS),2)),2)))
    return message

def expand(c,y):
    # multiplies the cipher text by the entire y vector 
    # Then we round the resultant vector entries to the nearest 
    # integer. Finally its resultant is made into a binlist 
    tmp = [roundFrac(c*yi) for yi in y] 
    
    fixedWidth = makeFixedWidthConverter(len(bin(max(tmp))))
    return map(lambda x: fixedWidth(intToBinList(x))[::-1],tmp)

def recrypt(c,y,encS,N):
    alpha, beta = getAlphaBeta(N)
    BlockSize = beta // alpha
    
    expC = expand(c,y)
    #print expC[0],
    #exit()
    print "*",
    print len(encS),len(expC),len(y),(alpha+beta)
    assert(len(encS) == len(expC))
    # there is no reason that these should not be equivelent in length
    
    li = reduce(lambda a,b:a+b,
                [map(lambda a: ski*a,cei) 
                 for ski,cei in zip(encS,expC)
                 ]
                )
    
    
    print "*",

    ly = split(li,BlockSize)
    # this is essentially used to change the dimmentions of our matrix
    # so that the y_i values are lined up 
    del li
   
    """
    ly = [sum(islice(li,BlockSize))          # 
          for i in range(alpha)]             # 
    """
    
    
    
    print "*",
    #exit()
    res = addReduce(ly)
    del ly
    print "*",
    print
    return res[1]+res[0] + c & 1
    

def testPkRecrypt(secure,message):
    
    N,P,Q = getNPQ(secure)
    (sk,S),(pk,y) = fheKeyGen(N)
    
    cipher  = fheEncrypt(message,pk,y,N)
    cipher  = [ i[0] for i in cipher ]
    
    cipher2 = fheEncrypt(message,pk,y,N)
    cipher2 = [ i[0] for i in cipher2 ]
    
    #c = pk.encrypt_pk
    pass


def go(secure,message):
    #
    N,P,Q = getNPQ(secure)
    (sk,S),(pk,y) = fheKeyGen(N)

    print "keygen   :: ",sk
    print "indexes  :: ",S

    print "-----------------------------"

    cipher = encrypt(message,pk,N) #fheEncrypt(message,pk,y,N)

    print "encrypt  :: ", [ int(i % 2) for i in cipher ]
    #print S
    #exit()
    #def encryptSk(sk,pk,y,N):
    encS = encryptSk(S,pk,N)
    print "*",
    
    
    #def recrypt(c,y,encS,alpha,beta):
    cipher2 = map(lambda x: recrypt(x,y,encS,N),cipher)

    print "rencrypt :: ", [ int(i % 2) for i in cipher2 ]

    print " d1      :: ", map(int,fheDecrypt(cipher,S))
    print " d2      :: ", map(int,fheDecrypt(cipher2,S))
    
    #print "atest   e:: ", [int(x%2) for x in stop2]

    #stop2 = [(x,multCipherHint(x,y)) for x in stop2]
    #print "atest   d:: ",map(lambda x: int(mods(x,sk)%2),stop2)
    
    """
    stop2 = [ i for i,_ in stop2]
    stop2 = cand(stop2,stop2)
    
    print "atest   e:: ", [int(x%2) for x in stop2]

    stop2 = [(x,multCipherHint(x,y)) for x in stop2]
    print "atest   d:: ", map(int,fheDecrypt(stop2,S))
    """

    #remess = map(int,fheDecrypt(cipher,S))
    #print "decrypt  :: ", remess

