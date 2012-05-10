from homo import *
import random

#Asym PHE Helper Functions
def privateKeyGen(P):
	return genKey(P)


def publicKeyGen(sk,N):
	N,P,Q=getNPQ(N)
	x=[0]*N
        encrypt = makeEncrypt(N,Q)
        public = encrypt(x,sk)
	maximal=0
	
	for i in public:
		if i>maximal:
			maximal=i
	#The Maximal pk element can't be even and it remainder sk can't be odd for some fucking reason
	#Can This Even Happen?
	if i % 2 ==0 or maximal %sk==1:
		public=publicKeyGen(sk,N)
        return public


def randomSubSetSum(pk):
	#Defaults to 2 rite now get over it
		return pk[random.randint(0,len(pk)-1)]+pk[random.randint(0,len(pk)-1)]
		
		
def asymKeyGen(N):
	N,P,Q=getNPQ(N)
	sk=privateKeyGen(P)
	pk=publicKeyGen(sk,N)
	return (sk,pk)
	


#message is an array pk is a public key array 
def encrypt(message,pk,N):
	cipher=[]
	rss=randomSubSetSum(pk)
	Mn,Mx = bitLims(N)
	for i in message:
		r2=2*(randint(Mn,Mx)//2)
		cipher.append(rss+r2 + i)
	return cipher

def decrypt(cipher,sk):
	message=[]
	for i in cipher:
		message.append(mods(i,sk)%2)
	return message

#TODO code correct a/b values
def getAlphaBeta(N):
	return (10,N**5)
	
#Generates key pairs and hints	
def fheKeyGen(N):
	N,P,Q=getNPQ(N)
	alpha,beta=getAlphaBeta(N)
	sk=privateKeyGen(P)
	pk=publicKeyGen(sk,N)
	
	hint=hintGen((1.0/sk),alpha)
	garbage=garbageGen(beta,alpha)
	y,S=hide(hint,garbage)
	
	return ((sk,S),(pk,y))
	
	
def hintGen(f,alpha):
	SparseSubset = []
	for i in range(alpha-1):
        	SparseSubset.append(random.random()*f)
        	f = f - SparseSubset[-1]
        SparseSubset.append(f)
        
        return SparseSubset
def garbageGen(beta,alpha):
	garbage=[]
	for i in range(beta-alpha):
		garbage.append(random.random()*2)
	return garbage
		
		
		
def hide(hint,garbage):
	S=[]
	for h in hint:
		
		index=random.randrange(0,len(garbage)-1)

		garbage.insert(index,h) 	
	for h in hint:
		S.append(garbage.index(h))
	return (garbage,S)
		
#Fhe Encrypt message is array pk is the set, y is the hidden sk, N is the security parameter
def fheEncrypt(message,pk,y,N):
	c=encrypt(message,pk,N)
	cipher=[]
	for i in range(len(c)):
		cipher.append((c[i],multCipherHint(c[i],y)))
	return cipher
	
#bultiplies a encuphered text by the hint
def multCipherHint(bit,y):
	for i in y:
		i*=bit
	return y		

#This needs Roundingz
def fheDecrypt(cy,S):
	message=[]
	for i in cy:
		c=i[0]
		y=i[1]
		message.append(abs( mods((mods(c,2) + mods(hintsum(y,S),2)),2)))
	return message
		
def hintsum(y,S):
	z=0.0
	for i in S:
		z+=y[i]
	return int(round(z))
	


def encryptSk(sk,pk,N):
	encS=[0]*len(pk[1])
	
	for i in sk[1]:
		encS[i]=1
	#print encS
	return encrypt(encS,pk[0],N)
	

#def fheRecrypt(cy,pk2,encS):
	#encrypt cy2 under pk2
	#encS is already encrypted under pk2
	#dot product cy[1] encS	
