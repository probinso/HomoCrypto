from helpers import *


"""
This section is for trivial circuits
"""
def bnot(a):
    return 1-a


def bxor(a,b):
    return a+b


def band(a,b):
    return a*b


def bnand(a,b):
    return bnot(band(a,b))


def bor(a,b):
    #bnand(bnand(a,a),bnand(b,b))
    return bnot(band(bnot(a),bnot(b)))


"""
This section is for multiplexed operations
"""
def mplex(G):
    # takes in a binary gate and turns it into
    # a multiplexer for that gate
    tG = lambda (a,b): G(a,b)

    """
    def plex(L):
        assert(len(L)>0)
        if len(L) == 2: return G(L[0],L[1])
        if len(L) == 1: return L[0]
        A = L[:len(L)//2]
        B = L[len(L)//2:]

        C = zip(A,B)
        out = map(tG,zip(A,B))

        if len(A)!=len(B):
            out.append(B[-1])
            
        return plex(out)
    """
    
    def plex(L):
        assert(len(L)>0)
        out = L
        while True:
        
            if len(out) == 2: return G(out[0],out[1])
            if len(out) == 1: return out[0]
            A = out[:len(out)//2]
            B = out[len(out)//2:]
            
            out = map(tG,zip(A,B))
            
            if len(A)!=len(B):
                out.append(B[-1])
            

    return plex


mxor,mand,mnand,mor = [mplex(G) for G in [bxor,band,bnand,bor]]


"""
This section is for single gate cross operations
"""
def cplex(G):
    # takes in a binary operator and turns it into
    # a cross circuit for two lists of equal size
    #
    # one list may be longer, as the remainder
    # will just be dropped from the longer
    tG = lambda (a,b):G(a,b)
    def plex(A,B):
        assert(len(A) > 0)
        return map(tG,zip(A,B))
    return plex


cxor,cand,cnand,cor = [cplex(G) for G in [bxor,band,bnand,bor]]

"""
This section is for arethmatic operators
"""
## Complex Operators ##
def myadd(L1,L2):
   def carry(A,B,C):
      # This is the carry logic that clark
      # provided for the adder
      return A*B+A*C+B*C

   convert = makeFixedWidthConverter(max(len(L1),len(L2))+1)
   # we choose the max length + 1 to satisfy carry bits, without
   #

   L1 = convert(L1)
   L2 = convert(L2)

   # apparently reverse() is an in-place
   # side-effects driven procedure
   #
   # also the carry bit gets way out of
   # controle. There should be a moduluo
   # however I have not gotten to that.
   Z = zip(L1,L2)[::-1]
   # the reverse is needed to preserve the
   # endian of this data.
   C = [0]

   for x in Z:
      C = [carry(x[0],x[1],C[0])] + C

   C = zip(L1,L2,C[1:])
   return map(lambda x: x[0]+x[1]+x[2],C)


def makeFixedAddr(D):
    def carry(A,B,C):
        # This is the carry logic that clark
        # provided for the adder
        return mxor([band(A,B),band(A,C),band(B,C)])

    toFixedWidth = makeFixedWidthConverter(D)

    def fixedAddr(L1,L2):
        # this is a fixed width adder for binary lists with
        # a signed bit head.
        L1 = toFixedWidth(L1)
        L2 = toFixedWidth(L2)

        Z = zip(L1,L2) #[::-1]
        # originally removed in place, but copying the list adds
        # to memory consumption
        Z.reverse()
        C = [0]
        for x in Z:
            C = [carry(x[0],x[1],C[0])]+C

        C = zip(L1,L2,C[1:]) # drop greatest digit

        return map(lambda (a,b,c):mxor([a,b,c]),C)

    return fixedAddr


Add16 = makeFixedAddr(16)
addReduce = mplex(Add16) # if this works i'll be so yoked !
# I was so yoked!

def makeMult():
    # positive integer multiplier ... couldn't get past
    # two's complement for multiply without quereying bits
    def identTop(L1,L2):
        # this is used to minimize volume of noise
        # in circuit. The smaller of two bit strings
        # should be treated as the bottom half of the
        # bit shift adder.
        Top = L1 # multiplicand
        Bot = L2 # multiplier
        if len(L1) < len(L2):
            Top = L2
            Bot = L1
        return (Top,Bot)

    tand = lambda (a,b) : band(a,b)

    def Mult(L1,L2):
        # bitwize multiplier
        # only works with positive numbers

        Top,Bot = identTop(L1,L2)    # makes circuit depth shorter

        Pairs =[ map(tand,
                     zip(Top,[bit]*len(Top)))
                     for bit in Bot[::-1]
                     ]

        #                   s = (T xor B) ... not used
        #          T  o  p
        #       x  B  o  t
        #       -----------
        #         Tt ot pt  ['Pairs' denotes these entries
        #      To oo po  0    without the s padding with
        # + TB oB pB  0  0    as represented by 'signed' ]
        # -----------------

        for i,_ in enumerate(Pairs):
            for j in range(i):
                Pairs[i].append(0)
                # this could be changed if we can insure
                # the numbers we are multiplying are all
                # positive.

        return reduce(lambda a,b: myadd(a,b),Pairs)
    return Mult


MULT = makeMult()


def makeMultB():
    def identTop(L1,L2):
        Top = L1 # multiplicand should be shorter
        Bot = L2 # multiplier   should be longer
        if len(L1)>len(L2):
            Top,Bot = Bot,Top
        return Top,Bot

    """
    def Mult(L1,L2):
        # This might be a minimal noise multiplier,
        #   It may be possible to shrink noise by
        #   adding opposing ends of the bitstream
        #   but I am unsure of this.
        Top,Bot = identTop(L1,L2)

        Val = [cand([t]*len(Bot),Bot) for t in Top][::-1]
        # the bits are reversed so that we can handle carying them better

        tmp = []
        if len(Val)%2 == 1:
            tmp = Val[-1]
            tmp = [tuple((tmp,[0]*len(tmp)))]
        else:
            tmp = []

        i = 0

        f = lambda (a,b): myadd(a,b+[0]*i)

        while len(Val) != 1:
            i+=1
            Val = zip(Val[::2],Val[1::2]) + tmp

            Val = map(f,Val)

            if len(Val)%2 == 1:
                tmp = Val[-1]
                tmp = [tuple((tmp,[0]*len(tmp) ))]
            else:
                tmp = []
        # I am getting one more bidget then I would like not sure
        #   why, but multiplier works w/ positive integers
        return Val[0]
    """
    
    tand = lambda (a,b): band(a,b)
    def Mult(L1,L2):
        # This might be a minimal noise multiplier,
        #   It may be possible to shrink noise by
        #   adding opposing ends of the bitstream
        #   but I am unsure of this.
        Top,Bot = identTop(L1,L2)

        Val = [ map(lambda x: band(t,x),Bot)+[0]*i for i,t in enumerate(Top) ]
        # the bits are reversed so that we can handle carying them better

        while True:
            acc = []
            i = 0
            if len(Val) == 1: return Val[0]
            while len(Val) > 1:
                if i % 2 == 0:
                    acc.append(Add16(Val[0],Val[-1]))
                else:
                    acc.insert(0,(Add16(Val[0],Val[1])))
                i+=1
                Val = Val[1:-1]
            i = 0
            Val = acc
            
    return Mult




MULTB = makeMultB()

"""
Others
"""
def search(L1,L2,acc):
    if len(L2)<len(L1):
        return acc

    List = [0 for i in acc]
    List[-1] = bnot(mor(cxor(L1,L2)))
    acc = Add16(acc,List)[1:]

    return search(L1,L2[8:],acc)

