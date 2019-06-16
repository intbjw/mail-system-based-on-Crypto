
import random, sys, os, rabinMiller, cryptomath

def main():
    print('生成秘钥文件')
    makeKeyFiles('al_sweigart', 1024)

def generateKey(keysize):
    # 生成密钥
    print('Generating p prime...')
    p = rabinMiller.generateLargePrime(keysize)
    print('Generating q prime...')
    q = rabinMiller.generateLargePrime(keysize)

    n = p * q
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        e = random.randrange(2*(keysize-1), 2**keysize)
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    print('Calculating d that is mod inverser of e...')
    d = cryptomath.findModInverse(e, (p - 1)*(q - 1))

    publicKey = (n, e)
    privateKey = (n, d)
    print('Public key:', publicKey)
    print('Private key:', privateKey)

    return (publicKey, privateKey)

def makeKeyFiles(name, keySize):
    # 生成密钥文件
    if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt'% (name)):
        sys.exit('WARNING: The file %spubkey.txt or %s_privkey.txt already exists! Use a different name or delete these files and re- run'
                 'this program.'% (name,name))
    publicKey,privateKey = generateKey(keySize)
    print()
    print('The public key is a %s and a %s digit number.' %(len(str(publicKey)),len(str(publicKey[1]))))
    print('Writing public key to file %s_pubkey.txt...' % name)
    fo = open('%s_pubkey.txt' % name,'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()

    print()
    print('The prvate key is a %s and a %s digit number.' % (len(str(publicKey[0])),len(str(publicKey[1]))))
    print('Writing public key to file %s_privkey.txt...' % name)
    fo = open('%s_privkey.txt' % name, 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fo.close()
if __name__ == '__main__':
    main()
