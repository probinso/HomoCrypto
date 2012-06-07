from asymhomo import encrypt
from helpers import intListToBinList
import os

with open("./gentry_pk.txt","r") as f:
    pk = f.read().split(",")
    pk = map(int,pk)
    f.closed

def jolly(word):
    binlist = intListToBinList(word)
    cipher = encrypt(binlist,pk,8)
    return cipher
