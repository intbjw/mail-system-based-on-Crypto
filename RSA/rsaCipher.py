# RSA Cipher
# RSA 密码
# http://inventwithpython.com/hacking (BSD Licensed)

import sys

# IMPORTANT: The block size MUST be less than or equal to the key size!
# (Note: The block size is in bytes, the key size is in bits. There
# are 8 bits in 1 byte.)
DEFAULT_BLOCK_SIZE = 128 # 128 bytes
BYTE_SIZE = 256 # One byte has 256 different values.

def main():
    # Runs a test that encrypts a message to a file or decrypts a message
    filename = 'encrypted_file.txt' # 需要加密或者解密的文件
    mode = 'decrypt' # 设置 'encrypt'加密 or 'decrypt'解密

    if mode == 'encrypt':
        # 需要加密的文本
        message = '''hello world!!!!!'''
        pubKeyFilename = 'al_sweigart_pubkey.txt'
        print('Encrypting and writing to %s...' % (filename))
        encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)

        print('Encrypted text:')
        print(encryptedText)

    elif mode == 'decrypt':
        privKeyFilename = 'al_sweigart_privkey.txt'
        print('Reading from %s and decrypting...' % (filename))
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)

        print('Decrypted text:')
        print(decryptedText)


def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    # 将字符串转换为整数快序列，每个整数表示128个（或者设置为任意块大小）字符串字符
    messageBytes = message.encode('ascii') # 将以ascii形式转换为二进制串

    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        # 计算文件的整数数值
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    # 将一串整数转换为源文本
    # 正确地转换最后一块整数块，需要原始消息的长度
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    # 将文本字符串转换为一串整数，并且加密每个整数块，通过公钥进行加密
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # ciphertext = plaintext ^ e mod n
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
    # 将加密后的整数块解密成源文本，正确的解密这个最后的整数块需要源文本的长度
    # 确保使用私钥进行解密
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    # 给出一个文件名，并从该文件中含有公钥或者私钥
    # 以元组的形式返回  (n,e) or (n,d)
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):
    # 从密钥文件中获取密钥，加密文本并将它保存成文件，返回值为加密后的文本
    keySize, n, e = readKeyFile(keyFilename)

    # 检查密钥的大小是否大于块的大小
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or less than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))


    # 对文本加密
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    # 将大整数转化为字符串
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    # 把加密后的文本写入输出文件中
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()
    # 同时返回加密文本
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    # 从密钥文件中获取密钥，并从文件中获取加密后的文本，然后对它进行解密
    # 返回值为解密后的文本字符串
    keySize, n, d = readKeyFile(keyFilename)


    # 从文件中获取文本的长度和加密的字符串
    fo = open(messageFilename)
    content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    # 检查密钥的大小是否大于块的大小
    if keySize < blockSize * 8: # * 8 to convert bytes to bits
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or less than the key size. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))

    # 将加密的文本转换为大整型
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    # 加密这个大整数
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)


# 程序的入口
# 主函数
if __name__ == '__main__':
    main()
