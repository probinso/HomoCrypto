#from fractions import Fraction
from django.shortcuts import render_to_response
from django.template import RequestContext
from HomoCrypto.program.helpers import *
import HomoCrypto.program.asymhomo
import HomoCrypto.program.client
#import os

with open('/home/homocrypto/rematch/homomorphic/HomoCrypto/program/gentry_pk.txt','r') as f:
	pk = f.read().split(',')
	pk = map(int,pk)
	#print len(pk)
        f.closed

"""
with open('/home/homocrypto/rematch/homomorphic/HomoCrypto/program/gentry_y.txt') as y:
	yv = y.read().split(',')
	yv = map(Fraction,yv)
	print "and print that y vectage!"
	y.closed
"""

def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

def encrypt(request):
	try:
		word = request.POST['search']
		binlist = intListToBinList(word)
	except:
		return render_to_response('index.html',{'s': ["No initial input"]}, context_instance=RequestContext(request))

	# sk,pk = HomoCrypto.program.asymhomo.fheKeyGen(8)
	
	try:
		cipher = HomoCrypto.program.asymhomo.encrypt(binlist, pk, 8)
		cipher = map(lambda x: str(x)[:-1],cipher)
	except:
		cipher = ["Encrypt Error"]

	try:
		HomoCrypto.program.client.sendciphertext(cipher)
	except:
		cipher = ["Hadoop listener is not running"] + cipher
		
	#dance party
	
        return render_to_response('index.html',{'s': cipher}, context_instance=RequestContext(request))

