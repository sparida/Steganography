#! /usr/bin/env python
#
# $Author$
# $Date$
# $HeadURL$
# $Revision$

# Version Info
# Python 2.7.3
# Pillow 2.6.1
# pycrypto 2.6.1

# Test script results in testExtendedSteganography.log

import base64
from Crypto.Cipher import AES
from PIL import Image
import re

from Steganography import Message, Steganography

class AesMessage(Message):
	def __init__(self, message, password):
		"""
		AESMessage constructor that initilaizes a AESMessage instance based on data provided. The data is verified for validity and appropriate errors raises in case of invalid data. The contructor takes a password and a message object to initialize member variables. All otehr functions are onherited from Message class in Steganography.py
		"""		
		import base64
		from Crypto.Cipher import AES
		from PIL import Image
		import re
		if message == None:
			raise ValueError('Message cannot be empty')
		elif password == '':
			raise ValueError('Password cannot be empty')	
		self.messageType = message.messageType
		self.msgStr = message.msgStr
		
		self.msgXML = message.getXmlString()
		self.msgB64 = message.msgB64
		self.msgSize = message.msgSize
		self.im = message.im
		self.msgEnc = None
		self.shouldDecrypt = message.isEncrypted
		
		self.isEncrypted = 'True'
		self.msgPwd = password
		self.aes = AES.new(self.msgPwd, AES.MODE_ECB)
		if (self.shouldDecrypt == 'True'):
			self.decryptMessage()
			
		else:
			self.loadMsg(self.messageType)
		
	def loadMsg(self, msgType):
		"""
		Calls the appropriate load message function based on message type
		"""
		if msgType == 'Text':
			self.loadTextFile()
		elif msgType == 'GrayImage':
			self.loadGrayImageFile()
		elif msgType == 'ColorImage':
			self.loadColorImageFile()
	
	def loadTextFile(self):
		"""
		Stores encrypted form of message text data in the Message object in as self.Enc in AESMessage object
		"""
		self.msgSize = str(len(self.msgStr))
		
		if (self.isEncrypted == 'True'):
			self.msgEnc = self.aes.encrypt(self.msgStr)
			self.msgB64 = self.convertUTF8ToBase64(bytearray(self.msgEnc))
		else:
			self.msgB64 = self.convertUTF8ToBase64(bytearray(self.msgStr))
	
	def loadGrayImageFile(self):
		"""
		Stores encrypted form of message grayscale image data in the Message object in as self.Enc in AESMessage object
		"""

		#a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
		#b = base64.b64encode(aes.encrypt(str(bytearray(a))))
		#c = list(bytearray(aes.decrypt(base64.b64decode(b))))
		#print a == c (True)

		
		k, l = self.im.size
		self.msgStr = []
		self.msgStr = list(self.im.getdata())
		self.msgSize = str('%s,%s'%(self.im.size[0], self.im.size[1]))
		
		if (self.isEncrypted == 'True'):
			self.msgEnc = self.aes.encrypt(str(bytearray(self.msgStr)))
			self.msgB64 = base64.b64encode(self.msgEnc)
		else:
			self.msgB64 = self.convertUTF8ToBase64(bytearray(self.msgStr))
		

	def loadColorImageFile(self):
		"""
		Stores encrypted form of message color image data in the Message object in as self.Enc in AESMessage object
		"""
		
		k, l = self.im.size
		self.msgStr = []
		self.msgStr = list(self.im.getdata(0)) + list(self.im.getdata(1)) + list(self.im.getdata(2))
		self.msgSize = str('%s,%s'%(self.im.size[0], self.im.size[1]))
		self.msgEnc = None
		
		if (self.isEncrypted == 'True'):
			self.msgEnc = self.aes.encrypt(str(bytearray(self.msgStr)))
			self.msgB64 = base64.b64encode(self.msgEnc)
		else:
			self.msgB64 = self.convertUTF8ToBase64(bytearray(self.msgStr))	
	
	def decryptMessage(self):
		"""
		Calls the appropriate decryption function based on message type 
		"""
		if self.messageType == "Text":
				self.msgStr = self.convertBase64ToUTF8(self.msgB64)
		elif self.messageType == "GrayImage":
				self.im = self.getIMFromB64()
		elif self.messageType == "ColorImage":
				self.im = self.getIMFromB64()
		
class ColorSteganography(Steganography):
	def __init__(self, imagePath, direction='horizontal'):
		
		"""
		Instantiates a ColorSteganography object based on embed direction and image to be used as steganomedium. Can handle only color images as steganomedium. All other functions are inherited from Steganography class in Steganography.py
		"""	
		import base64
		from PIL import Image
		from Crypto.Cipher import AES
		import re
		try:
			self.med = Image.open(imagePath)
		except:
			raise ValueError('Invalid File Name')
		if direction not in ['horizontal', 'vertical']:
			raise ValueError('Unknown Direction.')
		elif self.med.mode not in ['RGB']:
			raise TypeError('Not a Color Image')
		else:	
			self.dir = direction
			self.eMed = None
			self.medSize = self.med.size[0] * self.med.size[1] * 3


def main():
	password = 'Bold & Beautiful'
        sourcePath = 'files/color_mona' + '.png'
        expectedPath = 'files/color_mona_enc.xml'

        message = Message(filePath=sourcePath, messageType='ColorImage')
        encryptedMessage = AesMessage(message, password)
	"""
        with open('qwerty', 'w') as xmlFile:
            xmlString = encryptedMessage.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles('qwerty', expectedPath)

        print (actualTextFile == expectedTextFile)
	"""

if __name__ == "__main__":
	main()
