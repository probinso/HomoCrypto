from fractions import Fraction
from django.shortcuts import render_to_response
from django.template import RequestContext
from HomoCrypto.program.helpers import *
import HomoCrypto.program.asymhomo
import os

with open('/home/homocrypto/rematch/homomorphic/HomoCrypto/program/gentry_pk.txt','r') as f:
	pk = f.read().split(',')
	pk = map(int,pk)
	print len(pk)
        f.closed

"""
with open('/home/homocrypto/rematch/homomorphic/HomoCrypto/program/gentry_pk.txt') as y:
	yv = y.read().split(',')
	yv = map(Fraction,yv)
	print "and print that y vectage!"
	y.closed
"""

def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

def encrypt(request):
	word = request.POST['search']
        binlist = intListToBinList(word)
	
	# sk,pk = HomoCrypto.program.asymhomo.fheKeyGen(8)

	"""
	with open('/home/homocrypto/rematch/homomorphic/HomoCrypto/program/gentry_pk.txt','r') as f:
		pk = f.read().split(',')
		pk = map(int,pk)
	f.closed
	
	with open('/home/homocrypto/rematch/homomorphic/HomoCrypto/program/gentry_pk.txt') as y:
		yv = y.read().split(',')
		yv = map(Fraction,yv)
	y.closed
	"""

	cipher = HomoCrypto.program.asymhomo.encrypt(binlist, pk, 8)
	cipher = map(lambda x: str(x)[:-1],cipher)

	# os.system("140.160.137.13")
		
	# print "and dat shit be encrypted!"
	
        return render_to_response('index.html',{'s': cipher}, context_instance=RequestContext(request))

