from homo import *
import random
from fractions import Fraction
from math import ceil
from math import log

#Asym PHE Helper Functions
def privateKeyGen(P):
	return genKey(P)


def publicKeyGen(sk,N):
	N,P,Q=getNPQ(N)
	#x=[0]*N
	x=[0]*P
        encrypt = makeEncrypt(N,Q)
        public = encrypt(x,sk)
	"""
	maximal=0
	
	for i in public:
		if i>maximal:
			maximal=i
	#The Maximal pk element can't be even and it remainder sk can't be odd for some fucking reason
	#Can This Even Happen?
	if i % 2 ==0 or maximal % sk == 1:
		public=publicKeyGen(sk,N)
	"""
        return public


def randomSubSetSum(pk):
	#Defaults to 2 rite now get over it
	return sum([choice(pk) for i in range(2)])
	#return pk[random.randint(0,len(pk)-1)]+pk[random.randint(0,len(pk)-1)]

	
def asymKeyGen(N):
	N,P,Q=getNPQ(N)
	sk=privateKeyGen(P)
	pk=publicKeyGen(sk,N)
	return (sk,pk)


#message is an array pk is a public key array 
def encrypt(message,pk,N):
	"""
	cipher=[]
	rss=randomSubSetSum(pk)
	Mn,Mx = bitLims(N)
	for i in message:
		r2=2*(randint(Mn,Mx)//2)
		cipher.append(rss+r2 + i)
	#return cipher
	"""
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
	Mn,Mx = bitLims(N)
	rss = randomSubSetSum(pk)
	cipher = [rss+i for i in message]
	
	print "encrypted bits :: [",(cipher[0]%2),
	for x in cipher[1:]:
		print ",",x % 2,
	print "]"
	return cipher
	
	

def decrypt(cipher,sk):
	message=[]
	for i in cipher:
		message.append(mods(i,sk)%2)
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
	
	hint=hintGen((1.0/sk),alpha)
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
	f=Fraction(f)
	SparseSubset = []
	for i in range(alpha-1):
        	SparseSubset.append(Fraction(round(random.random()*f,int(ceil((log(alpha,2)+3))))))
        	f = f - SparseSubset[-1]
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
def multCipherHint(bit,y):
	
	for i in y:
		i*=bit
	return y
	##### FLAG
	#return [(x*bit)%2 for x in y]
	#return [x*bit for x in y]

#This needs Roundingz
def fheDecrypt(cy,S):
	"""
	  cy is the cypher tuples 
	"""
	message=[] 
	for i in cy:
		c=i[0] # cipher text
		y=i[1] # cipher text vector ... needs explaining
		#message.append(abs( mods((mods(c,2) + mods(hintsum(y,S),2)),2)))
		message.append((c%2)^hintsum(y,S)%2)
	return message

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


def go(secure,message):
	print message
	(sk,S),(pk,y) = fheKeyGen(secure)
	print "secret key :",sk
	print "public keys:",
	for i in pk:
		print i%2,
	print
	print "finished keygen"
	cipher = fheEncrypt(message,pk,y,secure)
	print "finished encrypt"
	print fheDecrypt(cipher,S)
