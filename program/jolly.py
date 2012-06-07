from asymhomo import encrypt

with open('./gentry_pk.txt','r') as f:
    pk = r.read().split(',')
    pk = map(int,pk)
    f.close()

def jolly(word):
    binlist = intToBinList(word)
    cipher = encrypt(binlist,pk,8)
    return cipher
