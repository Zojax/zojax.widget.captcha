# xor implementation with PyCrypto interface
from itertools import izip, cycle

def new(key):
    return Xor(key)


class Xor:
    def __init__(self, key):
        self.__key = key

    def __xor(self, s):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(s, cycle(self.__key)))

    def __normkey(self, s):
        self.__key = self.__key * (len(s) / len(self.__key))

    def encrypt(self, s):
        self.__normkey(s)
        return self.__xor(s)

    decrypt = encrypt
