
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
    return plex

mxor,mand,mnand,mor = [mplex(G) for G in [bxor,band,bnand,bor]]

"""
This section is for single gate cross operations
"""

def cplex(G):
    # takes in a binary operator and turns it into
    # a cross circuit for two lists of equal size 
    #
    # the second list may be larger, as the remainder
    # will just be dropped
    tG = lambda (a,b):G(a,b)
    def plex(A,B):
        assert(len(A) > 0)
        return map(tg,zip(A,B))
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
   
   
   C = zip([0]+L1,[0]+L2,C)
   return map(lambda x: x[0]+x[1]+x[2],C)

def makeFixedAddr(D):
    def carry(A,B,C):
        # This is the carry logic that clark
        # provided for the adder
        return mxor([band(A,B),band(A,C),band(B,C)])
    
    def toFixedWidth(L):
        # we assume that the input comes in with 
        # a leading bit denoting the sign
        store = [L[0]]*D
        store[-1*len(L):] = L[::]
        return store
    
    def fixedAddr(L1,L2):
        L1 = toFixedWidth(L1)
        L2 = toFixedWidth(L2)
        
        Z = zip(L1,L2)        
        C = [0]
        for x in Z:
            C = C + [carry(x[0],x[1],C[-1])]
            
        C = zip(L1,L2,C[1:]) # drop greatest digit 
        
        return map(lambda (a,b,c):mxor([a,b,c]),C)

    return fixedAddr



"""
Others
"""
def search(L1,L2,acc,Zeros):
    
    if len(L2)<len(L1):
        return acc
    
    List = myxor(L1,L2)
    Zeros[-1]= bnot(reduce(lambda x,y: bor(x,y),List))
    acc = myadd(acc,Zeros)[1:]
    
    return search(L1,L2[8:],acc,Zeros)

