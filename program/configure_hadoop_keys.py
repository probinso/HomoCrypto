

#A simple script that can read and write generated Gentry keys
import asymhomo
from fractions import Fraction
from helpers import *
def makeAndWriteHadoopKeys():
    sk,pk=asymhomo.fheKeyGen(8)
    sk_file=file("gentry_sk.txt","w")
    for i in range(len(sk[1])):
        if i==len(sk[1])-1:
            sk_file.write(str(sk[1][i]))
        else:
            sk_file.write(str(sk[1][i]))
            sk_file.write(",")
    
    pk_file=file("gentry_pk.txt","w")
    
    for i in range(len(pk[0])):
        if i==len(pk[0])-1:
            pk_file.write(str(pk[0][i]))
        else:
            pk_file.write(str(pk[0][i]))
            pk_file.write(",")

    y_file=file("gentry_y.txt","w")
    for i in range(len(pk[1])):
        if i==len(pk[1])-1:
            y_file.write(str(pk[1][i]))
        else:
            y_file.write(str(pk[1][i]))
            y_file.write(",")

    sk_file.close()
    pk_file.close()
    y_file.close()


def makebible():
	with open("input_data/jesus_fucking_christ.txt") as content_file:
	    content = content_file.read()

	content = intListToBinList(content)
	biblebit = file("/tmp/biblebit.txt","w")

	for x in content:
		biblebit.write(str(x))
	biblebit.close()
	



def readPublicKeys():
#	try:
		pk_file=open("gentry_pk.txt")
		y_file=open("gentry_y.txt")

		pk0=[]
		pk1=[]

		x=pk_file.read().split(",")
		for i in x:
			pk0.append(int(i))



		x=y_file.read().split(",")
		for i in x:
			fr=i.split("/")
			pk1.append(Fraction(int(fr[0].strip()),int(fr[1].strip())))	
		return pk0,pk1
#	except:
#		print "File Error. Place the keys in the same folder as the script plz" 
#		return
