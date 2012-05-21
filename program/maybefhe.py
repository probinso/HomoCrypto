
#Let's try this
encS=asy.encryptSk(sk,pk,8)

#Encrypt a message
cipher=asy.fheEncrypt([1,1,0,1],pk[0],pk[1],8)

for bit in cipher:

    r=asy.dotProduct(encS,cipher[0][1])
    bit=(r,asy.multCipherHint(r,pk[1]))

    

asy.fheDecrypt(cipher,sk[1])
