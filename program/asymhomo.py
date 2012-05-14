from homo import *
import random
from fractions import Fraction
from math import ceil
from math import log

#Asym PHE Helper Functions
def privateKeyGen(P):
	return genKey(P)


def distribute(sk,N,Q):
	q=random.randrange(0,(2**((N**5)))//sk)
	r=random.randrange(-1*(2**N),2**N)
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
	#return pk[random.randint(0,len(pk)-1)]+pk[random.randint(0,len(pk)-1)]


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
	"""
	"""
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
	"""
	return (10,N**5)

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
	#f=Fraction(f)

	F = lambda x: Fraction(round(
			random.random(),     # produce random number \in (0,1)
			int(log(alpha,2)+3+1)# to this many degrees of accuracy
			))*x# then cast it as a Fraction
	"""
	  we move *x to the outside of the function above because we
	  want to insure that the function does not round to zero
	  before the round function can be applied. 
	"""
	"""
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
	for i in range(beta-alpha):
		garbage.append(Fraction(round(random.random()*2,int(ceil((log(alpha,2)+3))))))
	
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
	#S=[] # [0]*(len(garbage)+len(hint))
	for h in hint:	
		index=random.randrange(0,len(garbage)-1)
		garbage.insert(index,h)
	
	S = [garbage.index(h) for h in hint]
	#for h in hint:
	#	S.append(garbage.index(h))
	return (garbage,S)

#Fhe Encrypt message is array pk is the set, y is the hidden sk, N is the security parameter
def fheEncrypt(message,pk,y,N):
	"""
	  pk = one of the public keys 
	  y  = the set of values for subset-sum security 
	  N  = security parameter 
	"""
	
	c = encrypt(message,pk,N)
	cipher = [(x,multCipherHint(x,y)) for x in c]
	# code below has been abandoned
	#for i in range(len(c)):
	#	cipher.append((c[i],multCipherHint(c[i],y)))
	return cipher

#bultiplies a encuphered text by the hint
def multCipherHint(encbit,y):
	ctotup = [encbit* x for x in y]
	return ctotup
	##### FLAG
	#return [(x*bit)%2 for x in y]
	#return [x*bit for x in y]

#This needs Roundingz
def fheDecrypt(cy,S):
	"""
	  tupples?
	"""
	
	message=[((x[0]%2)^(hintsum(x[1],S) %2))%2 for x in cy]
	
	return message
	#for i in cy:
	#	c=i[0] # cipher text
	#	y=i[1] # cipher text vector ... needs explaining
	#	#message.append(abs( mods((mods(c,2) + mods(hintsum(y,S),2)),2)))
	#	message.append((c%2)^hintsum(y,S)%2)
	#return message

#This is doing the summing the wrong values
def hintsum(y,S):
	#z=0.0
	#for i in S:
	#	z+=y[i]
	return int(sum([y[i] for i in S]))
	#return int(round(z))

def encryptSk(sk,pk,N):
	encS=[0]*len(pk[1])
	
	for i in sk[1]:
		encS[i]=1
	#print encS
	return encrypt(encS,pk[0],N)
	

def dotProduct(L1,L2):
	sp=0
	for i in range(len(L1)):
		sp+=L1[i]*L2[i]
	return sp
			     
#def fheRecrypt(cy,y,pk2,encS,N):
	
	#Encrypt each cipher text bit in cy with pk. Reset each ciphered bit's Hint 
	#Vector by multiplying by the newly encrypted ciphertext
#	for i in cy:
#		encrypt([i[0]],pk2,y,N)[0]
		
	
	#CY is now doubly encrypted under pk1 and pk2.
#	for i in cy:
#		i[0]=dotProduct(i[1],encS)
	
#	return cy		
	#encS is already encrypted under pk2
	#dot product cy[1] encS	


def intToBinList(i):
    ret=[]
    while(i !=0):
            ret.append(i %2)
            i=i/2
    return list(reversed(ret))


def binListToInt(l):
    s=0
    l=list(reversed(l))
    for i in range(len(l)):
            s+=l[i]*2**i
    return s
			     
#Recrypt cy in place, return refreashed Ciphertext Tuples
def fheRecrypt(cy,y,pk,encS,N):
	
	for i in cy:
		ciphered=intToBinList(cy[0])
		#Do an FHE encrypt with an already chosen key
		ciphered=doubleEncrypt(cipher,pk,y,N)
		message=doubleDecrypt(cipher,encS)
		i[0]=binListToInt(message)
		i[1]=multCipherHint(i[0],y)
	return cy


#FHE Encrypt with Given pk rather than rss p
def doubleEncrypt(cipher,pk,y,N):
        c=encrypt(message,pk,N)
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
	
def go(secure,message):
	N,P,Q=getNPQ(secure)
	"""print message
	(sk,S),(pk,y) = fheKeyGen(secure)
	print "secret key :",sk
	#print "public keys:",
	#for i in pk:
	#	print i%2,
	print
	print "finished keygen"
	cipher = fheEncrypt(message,pk,y,secure)
	print "finished encrypt"
	print fheDecrypt(cipher,S)"""
	
	print "Message=", message
	
	sk=privateKeyGen(P)
	print "Finished SK Gen"
	pk=publicKeyGen(sk,N)
	print "public keys :: ", [x % 2 for x in pk[:5]]
	print "Finished Key Gens"
	cipher=encrypt(message,pk,N)
	print "finished Encrypt"
	print "Decrypted Message : ",decrypt(cipher,sk)
