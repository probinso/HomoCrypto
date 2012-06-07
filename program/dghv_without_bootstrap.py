

import asymhomo
import homo



def fheKeyGen(N):
    pass

def fheEncrypt(pk,m):
    return asymhomo.fheEncrypt(m,pk,8)


def fheDecrypt(sk,c):
    #if c is under modulus pj output c%pj%2
    pass

def fheAdd(pk,c1,c2):
    #line up c1,c2 modulus with i
    #add c1,c2
    #refresh the sum
    pass

def fheMult(pk,c1,c2):
    #refresh to align modulus
    #multiply
    #refresh result
    pass

def fheRefresh(pk,c3):
    #return switchKey(pk,c)
