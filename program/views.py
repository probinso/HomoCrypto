from fractions import Fraction
from django.shortcuts import render_to_response
from django.template import RequestContext
from HomoCrypto.program.helpers import *
import HomoCrypto.program.asymhomo

def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

def encrypt(request):
	word = request.POST['search']
        binlist = intListToBinList(word)
	
	# sk,pk = HomoCrypto.program.asymhomo.fheKeyGen(8)

	with open('/home/homocrypto/rematch/homomorphic/HomoCrypto/program/gentry_pk.txt','r') as f:
		pk = f.read().split(',')
		pk = map(int,pk)
	f.closed

	print "read dat pk!"

	with open('/home/homocrypto/rematch/homomorphic/HomoCrypto/program/gentry_pk.txt') as y:
		yv = y.read().split(',')
		yv = map(Fraction,yv)
	y.closed
	
	print "and dat y vectage!"

	cipher = HomoCrypto.program.asymhomo.fheEncrypt(binlist, pk, yv, 8)
		


	
	

        newword = wordBinListToString(binlist)
	
        return render_to_response('index.html',{'s': pk[0]}, context_instance=RequestContext(request))
