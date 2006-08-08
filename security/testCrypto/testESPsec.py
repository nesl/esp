#!/usr/bin/env python

import time, os, sys
sys.path.append("../../xml/")
import espml
import StringIO

from Crypto.Cipher import DES
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.Cipher import Blowfish
from Crypto.Cipher import RC5
from Crypto.PublicKey import RSA
from Crypto.PublicKey import DSA
from Crypto.Hash import MD5
from Crypto.Util import randpool

class testESPsec:

	def getSymTimings(self, testString):

		""" Executes the different types of symetric encryption algorithms on given string """

                # RSA
		rp = randpool.RandomPool()
                t1 = time.time()
                rsaKey = RSA.generate(1024, rp.get_bytes)
                t2 = time.time()
                print 'RSA key generation took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = rsaKey.encrypt(testString,"")
                t2 = time.time()
                print 'RSA encryption took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = rsaKey.decrypt(encString)
                t2 = time.time()
                print 'RSA decryption took: %0.3fms.' % ((t2-t1)*1000.)

                # DSA
                rp = randpool.RandomPool()
                t1 = time.time()
                dsaKey = DSA.generate(1024, rp.get_bytes)
                t2 = time.time()
                print 'DSA key generation took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = dsaKey.sign(testString,1024)
                t2 = time.time()
                print 'DSA signing took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
		hash = MD5.new(testString).digest()
                encString = dsaKey.verify(hash,encString)
                t2 = time.time()
                print 'DSA verifying took: %0.3fms.' % ((t2-t1)*1000.)

		# AES
		t1 = time.time()
		aesKey = AES.new('abcdabcdabcdabcdabcdabcdabcdabcd')
		t2 = time.time()
		print 'AES key generation took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = aesKey.encrypt(testString)
                t2 = time.time()
                print 'AES encryption took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = aesKey.decrypt(encString)
                t2 = time.time()
                print 'AES decryption took: %0.3fms.' % ((t2-t1)*1000.)

		# DES
                t1 = time.time()
                desKey = DES.new('abcdabcd')
                t2 = time.time()
                print 'DES key generation took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = desKey.encrypt(testString)
                t2 = time.time()
                print 'DES encryption took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = desKey.decrypt(encString)
                t2 = time.time()
                print 'DES decryption took: %0.3fms.' % ((t2-t1)*1000.)

		# DES3
                t1 = time.time()
                des3Key = DES3.new('abcdabcdabcdabcd')
                t2 = time.time()
                print 'DES3 key generation took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = des3Key.encrypt(testString)
                t2 = time.time()
                print 'DES3 encryption took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = des3Key.decrypt(encString)
                t2 = time.time()
                print 'DES3 decryption took: %0.3fms.' % ((t2-t1)*1000.)

		# Blowfish
                t1 = time.time()
                blowfishKey = Blowfish.new('abcdabcdabcdabcdabcdabcdabcdabcd')
                t2 = time.time()
                print 'Blowfish key generation took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = blowfishKey.encrypt(testString)
                t2 = time.time()
                print 'Blowfish encryption took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = blowfishKey.decrypt(encString)
                t2 = time.time()
                print 'Blowfish decryption took: %0.3fms.' % ((t2-t1)*1000.)

		# RC5
                t1 = time.time()
                rc5Key = RC5.new('abcdabcdabcdabcd')
                t2 = time.time()
                print 'RC5 key generation took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = rc5Key.encrypt(testString)
                t2 = time.time()
                print 'RC5 encryption took: %0.3fms.' % ((t2-t1)*1000.)

                t1 = time.time()
                encString = rc5Key.decrypt(encString)
                t2 = time.time()
                print 'RC5 decryption took: %0.3fms.' % ((t2-t1)*1000.)


if __name__ == '__main__':

	security = testESPsec()
	testString = "a" * 128
	#print testString
	security.getSymTimings(testString)
