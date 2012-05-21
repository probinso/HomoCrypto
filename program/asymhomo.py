from homo import *
import random
from fractions import Fraction
from math import ceil
from math import log

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
	
	c = encrypt(message,pk,N)
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
	
	message=[((x[0]%2)+(hintsum(x[1],S) %2))%2 for x in cy]
	
	return message
	#for i in cy:
	#	c=i[0] # cipher text
	#	y=i[1] # cipher text vector ... needs explaining
	#	#message.append(abs( mods((mods(c,2) + mods(hintsum(y,S),2)),2)))
	#	message.append((c%2)^hintsum(y,S)%2)
	#return message


def roundFrac(x):
	y = int(x)
	if y - x > Fraction(1,2):
		y+=1
	return y

#This is doing the summing the wrong values
def hintsum(y,S):
	#z=0.0
	#for i in S:
	#	z+=y[i]
	dasum=sum([y[i] for i in S])
	x=int(dasum)
	dasum-=x
	if(dasum-Fraction(1,2)>0):
		x+=1
	return x
	#return int(round(z))

#Used to Ecnrypt the Secret Key List with a new public Key

def encryptSk(sk,pk,N):
#the Sk list is a bunch of indecies. In order to do a recrypt it would need to be 
#A Vector of 1's and zeros as Gentry Described. This function uses the public key to encrypt the secret key
#and returns encS. Client would need to make this and send it to the server
	encS=[0]*len(pk[1])
	#print"Length of encS is",len(encS)
	x=0
	for i in sk[1]:
		
	#	print "On Round ",x
		x+=1
		encS[i]=1
	
	return encrypt(encS,pk[0],N)
	
#Given two equal length lists dot product them. Used by FHE Recrypt to do the summation of Y vector
#And the encrypted S Vector
def dotProduct(L1,L2):
	sp=0
	
	for i in range(len(L1)):
		sp+=L1[i]*L2[i]
	return sp
			     


def intToBinList(i):
    
    return map(int,list(bin(i))[2:])


def binListToInt(l):
    return int(''.join(map(str,l)),2)
			     
#Recrypt cy in place, return refreashed Ciphertext Tuples
#CY is a list of tuples. cy[0][0] is an encrypted bit cy[0][1] is it's y vector
#def fheDumbRecrypt(cy,y,pk,N):
#	apk=pk[0]
	
#	for  c in cy:
#		c[0] = c[0] - roundFrac(Fraction(sum(map(*,zip (c[0],y))),apk))
	
	
def fheRecrypt(cy,pk,encS,N):
	"""FHE Recrypt works as follows:
	*Convert Each Cipher bit into it's binary representation. If i[0] is a base ten integer representing a bit, it's 
	Bitwise representation is a list of zero's and ones. there are lg2(i[0
	elements in the list
	*Given that bitwise representaiton encrypt each bit. The given cipher bit is now doubly encrypted
	*Given the doubly encrypted list, Decrypted it using the encrypted sk 
	ector. The result should be a list of bits
	that sum up to the original cipher. 
	*Use the binlistToInt helper function to turn it back into a base 10 integer
	representing the original encrypted bit"""
	for i in range(len(cy)):
		fresh=int((cy[i][0])-mods(dotProduct(cy[i][1],encS),pk[0][0]))	 
		
		cy[i]=(fresh,multCipherHint(fresh,pk[1]))
		#ciphered=intToBinList(i[0])
		#Do an FHE encrypt with an already chosen key
		#ciphered=doubleEncrypt(ciphered,pk,y,N)
		#message=doubleDecrypt(ciphered,encS)
		#Extract the 
		#i[0]=binListToInt(message)
		#i[1]=multCipherHint(i[0],y)
	return cy


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
