from homo import *
import random
from fractions import Fraction
from math import ceil
from math import log
from helpers import *

debug=True
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
def encrypt(message,pk,y,N):
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
	return (10,N**2)

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
	
	c = encrypt(message,pk,y,N)
	cipher = [(x,multCipherHint(x,y)) for x in c]
	# code below has been abandoned
	#for i in range(len(c)):
	#	cipher.append((c[i],multCipherHint(c[i],y)))
	return cipher

#bultiplies a encuphered text by the hint
def multCipherHint(encbit,y):
	ctotup = [(encbit* x)%2 for x in y]
	return ctotup
	##### FLAG
	#return [(x*bit)%2 for x in y]
	#return [x*bit for x in y]

#This needs Roundingz
def fheDecrypt(cy,S):
	"""
	  tupples?
	"""
	
	
	
	
	#message=[  (x[0]%2 + hintsum(x[1],S)) %2 for x in cy] # this is wrong
	message=[((x[0]%2)+(hintsum(x[1],S) %2))%2 for x in cy]
	
	
	return message
	#for i in cy:
	#	c=i[0] # cipher text
	#	y=i[1] # cipher text vector ... needs explaining
	#	#message.append(abs( mods((mods(c,2) + mods(hintsum(y,S),2)),2)))
	#	message.append((c%2)^hintsum(y,S)%2)
	#return message

"""
def roundFrac(x):
	y = int(x)
	#print y
	if y - x > Fraction(1,2):
		y+=1
	return y
"""

#This is doing the summing the wrong values
def hintsum(y,S):
	
	val = roundFrac(sum([y[i] for i in S]))
	return val


#Used to Ecnrypt the Secret Key List with a new public Key

def encryptSk(sk,pk,y,N):
#the Sk list is a bunch of indecies. In order to do a recrypt it would need to be 
#A Vector of 1's and zeros as Gentry Described. This function uses the public key to encrypt the secret key
#and returns encS. Client would need to make this and send it to the server
	encS=[0]*len(y)
	
	for i in sk:
		encS[i]=1
	
	return encrypt(encS,pk,y,N)

#Recrypt cy in place, return refreashed Ciphertext Tuples
#CY is a list of tuples. cy[0][0] is an encrypted bit cy[0][1] is it's y vector
#def fheDumbRecrypt(cy,y,pk,N):
#	apk=pk[0]
	
#	for  c in cy:
#		c[0] = c[0] - roundFrac(Fraction(sum(map(*,zip (c[0],y))),apk))
	
	
def fheRecrypt(cy,pk,y,encS,N):
	"""
	FHE Recrypt works as follows:
	"""
	
	# fhedecrypt
	#message=[((x[0]%2)+(hintsum(x[1],S) %2))%2 for x in cy]
	
	# hintsum
	#val = roundFrac(sum([y[i] for i in S]))
	
	
	"""
	for (i= 0; i < S_1; i++){
	  d = (B_j * c mod 2p ) // note that d \isin [0,2)
	  for (j = 0; j < T; j++){
	    C_i,j = encrypt(floor(d))*c_j mod p
	    d = (d - floor(d))*2
	    
	"""
	
	cout = cy[::] 
	
	
	intToBinList(i)
	
	
	"""
	
	
	for i,encBit in enumerate(cout):
		fresh = encBit[0] #-mods(dotProduct(encBit[1],encS),pk[0])
		
		
		
		
		#fresh=int((cy[i][0])-mods(dotProduct(cy[i][1],encS),pk[0][0])) 
		
		#cout[i] = (fresh ,[roundFrac(fresh * x) for x in y])
		cout[i] = (fresh,multCipherHint(encBit[0],y))
			   
		
		#cy[i]=(fresh,multCipherHint(fresh,pk[1]))
		
		
		
		#ciphered=intToBinList(i[0])
		#Do an FHE encrypt with an already chosen key
		#ciphered=doubleEncrypt(ciphered,pk,y,N)
		#message=doubleDecrypt(ciphered,encS)
		#Extract the 
		#i[0]=binListToInt(message)
		#i[1]=multCipherHint(i[0],y)
	print " input -> ",type(cy),type(cy[0]),type(cy[0][0])
	print "output -> ",type(cout),type(cout[0]),type(cout[0][0])
	"""
	return cout


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
	
def go(secure,message):
	#
	N,P,Q = getNPQ(secure)
	(sk,S),(pk,y) = fheKeyGen(N)
	
	print "keygen   :: ",sk
	print "indexes  :: ",S
	
	print "-----------------------------"
	
	cipher = fheEncrypt(message,pk,y,N)
	
	print "encrypt  :: ", [int(i[0] %2) for i in cipher]
	
	remess = map(int,fheDecrypt(cipher,S))
	print "decrypt  :: ", remess
	
