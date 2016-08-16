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

# Test script results in testSteganography.log


import base64
from Crypto.Cipher import AES
from PIL import Image
import re


class Message():
	def __init__(self, **kwargs):
		
		"""
		Message constructor that initilaizes a message instance based on data provided. The data is verified for validity and appropriate errors raises in case of invalid data. There are two different forms the contructor can take and both cases are handled.  
		"""

		import base64
		from PIL import Image
		from Crypto.Cipher import AES
		import re
		self.messageType = None
		self.msgStr = None
		self.msgEnc = None
		self.msgXML = None
		self.msgB64 = None
		self.msgSize = None
		self.msgEnc = None
		self.im = None
		self.isEncrypted = 'False'
		self.msgPwd = '1234567891234567'
		self.aes = AES.new(self.msgPwd, AES.MODE_ECB)

		if (len(kwargs) == 1) and ('XmlString' in kwargs.keys()):
			
			self.msgXML = kwargs['XmlString']
			r_str = r'^(<\?xml version="1.0" encoding="UTF-8"\?>\n)'
			r_str = r_str + r'<message type="(?P<mType>(GrayImage|ColorImage|Text))" size="(?P<size>(([0-9]+)|([0-9]+,[0-9]+)))" encrypted="(?P<enc>(False|True))">\n'
			r_str = r_str + r'(?P<msg>.*)\n'
			r_str = r_str + r'</message>' 
		
			if re.match(r_str, self.msgXML):
				r = re.match(r_str, self.msgXML)
				self.messageType = r.group('mType')
				self.msgSize = r.group('size')
				self.isEncrypted = r.group('enc')
				self.msgB64 = r.group('msg')
				if self.messageType == "Text":
					self.msgStr = self.convertBase64ToUTF8(self.msgB64)
				elif self.messageType == "GrayImage":
					self.im = self.getIMFromB64()
				elif self.messageType == "ColorImage":
					self.im = self.getIMFromB64()
				else:
					raise TypeError('Invalid Message Type')

		elif (len(kwargs) == 2) and ('filePath' in kwargs.keys()) and ('messageType' in kwargs.keys()):
			if kwargs['messageType'] in ['Text', 'GrayImage', 'ColorImage']:
				self.messageType = kwargs['messageType']
				self.filePath = kwargs['filePath']
			
				try:
		
					self.loadMsg(self.messageType, self.filePath)
				except:
					raise ValueError('Invalid File Name')
			else:
				raise ValueError('Invalid Message Type.')
		else:
			raise ValueError('Missing Arguments or Argument Types.')
	
	
	def loadMsg(self, msgType, filePath):
		"""
		Calls te appropriate load message function based on message type
		"""
		if msgType == 'Text':
			self.loadTextFile(filePath)
		elif msgType == 'GrayImage':
			self.loadGrayImageFile(filePath)
		elif msgType == 'ColorImage':
			self.loadColorImageFile(filePath)
	
	def loadTextFile(self, filePath):
		"""
		Loads a text file based on filePath provided
		"""
		with open(filePath, 'r') as f:
			self.msgStr = f.read()
		self.msgSize = str(len(self.msgStr))
		
		if (self.isEncrypted == 'True'):
			self.msgEnc = self.aes.encrypt(self.msgStr)
			self.msgB64 = self.convertUTF8ToBase64(bytearray(self.msgEnc))
		else:
			self.msgB64 = self.convertUTF8ToBase64(bytearray(self.msgStr))
	
	def loadGrayImageFile(self, filePath):
		"""
		Loads a Grayscale Image based on filePath
		"""
		#a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
		#b = base64.b64encode(aes.encrypt(str(bytearray(a))))
		#c = list(bytearray(aes.decrypt(base64.b64decode(b))))
		#print a == c (True)

		self.im = Image.open(filePath)
		k, l = self.im.size
		self.msgStr = []
		self.msgStr = list(self.im.getdata())
		self.msgSize = str('%s,%s'%(self.im.size[0], self.im.size[1]))
		
		if (self.isEncrypted == 'True'):
			self.msgEnc = self.aes.encrypt(str(bytearray(self.msgStr)))
			self.msgB64 = base64.b64encode(self.msgEnc)
		else:
			self.msgB64 = self.convertUTF8ToBase64(bytearray(self.msgStr))
		

	def loadColorImageFile(self, filePath):
		"""
		Loads a Color Iage based on provided filePath
		"""
		self.im = Image.open(filePath)
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
	
	def getMessageSize(self):
		"""
		Returns the size of the XML representaion of the message. Used to judge if steganomdeium is large enough to hold XML representation odf message.
		"""
		return len(self.getXmlString())
	
	def saveToImage(self, targetImagePath):
		"""
		If message contains image and is of image type saves a copy of the image to specified target path.
		Raises approprate exceptions if required conditions are not met.
		"""
		
		if self.im == None and self.msgStr == None:
			raise Exception('No data in message')
		elif self.messageType not in ['GrayImage', 'ColorImage']:
			raise TypeError('Message Type is not Image')
		else:
			try:
				self.im.save(targetImagePath)
			except KeyError:
				self.im.save(targetImagePath + '.png')
			except Exception as e:
				pass
	
	def saveToTextFile(self, targetTextFilePath):
		"""
		If message contains text and is of text type saves a copy of the text to specified target path.
		Raises approprate exceptions if required conditions are not met.
		"""

		if self.msgStr == None and self.im == None:	
			
			raise Exception('No data in message')
		elif self.messageType != 'Text':
			raise TypeError('Message Type is not Text')
		else:
			g = open(targetTextFilePath, 'w')
			g.write(self.msgStr)
			g.close
	
	def saveToTarget(self, targetPath):
		"""
		Calls appropriate sae function based on message type. Does not raise errors by itself.
		"""
		if self.messageType == 'Text':
			self.saveToTextFile(targetPath)
		elif self.messageType == 'GrayImage':
			self.saveToImage(targetPath)
		elif self.messageType == 'ColorImage':
			self.saveToImage(targetPath)
	
	def getXmlString(self):
		"""
		Return the xml representation of the message from its base64 encoded form. XML includes message size, message type, whether encrypted or not and base64 representation of message.
		"""
		if self.msgB64 == None:
			raise Exception('No message to provide XML.')
		elif self.msgB64 != None and self.msgStr != None:
			output = '<?xml version="1.0" encoding="UTF-8"?>\n'
			output = output + '<message type="%s" size="%s" encrypted="%s">\n'%(self.messageType, self.msgSize, self.isEncrypted)
			output = output + self.msgB64 + '\n'
			output = output + '</message>'
			self.msgXML = output
			return output
		elif self.msgB64 != None and self.msgStr == None:
			return self.msgXML
	
	def getXMLString(self):
		"""
		Return the xml representation of the message from its base64 encoded form. XML includes message size, message type, whether encrypted or not and base64 representation of message.
		"""
		self.getXmlString()			
	
	def convertUTF8ToBase64(self, msg):
		"""
		Returns base 64 representation of a unicode formatted string
		"""
		msg64 = base64.standard_b64encode(msg)
		return msg64
	
	def convertBase64ToUTF8(self, msg64):
		"""
		Returns unicode representation of a base 64 string
		If message in ecnrypted, decrypts it before returning
		"""
		msg = base64.b64decode(msg64)
		self.msgEnc = msg
		if (self.isEncrypted == 'True'):
			msg = self.aes.decrypt(msg)
		return msg

	def getIMFromB64(self):
		"""
		Converts the base 64 represtation of an image into the appropriate image. (Color or Grayscale). If message is encrypted, converts to uicode, decrypts and then proceeds with unicode to image conversion.
		"""
		size = self.msgSize.split(',')
		w = int(size[0])
		h = int(size[1])
		if(self.isEncrypted == 'True'):
			i_list = list(bytearray(self.aes.decrypt(base64.b64decode(self.msgB64))))
		else:
			i_list = list(bytearray(base64.b64decode(self.msgB64)))
		
		if self.messageType == 'GrayImage':
			im = Image.new('L', (w, h))
			count = 0
			for i in range(len(i_list)):
				x = count % w
				y = (count - x) / w
				im.putpixel((x, y), i_list[i])
				count = count + 1
		elif self.messageType == 'ColorImage':
			im = Image.new('RGB', (w, h))
			count = 0
			for i in range(len(i_list)/3):
				x = count % w
				y = (count - x) / w
				rgb = (i_list[i], i_list[i + (1*w*h)], i_list[i + (2*w*h)])
				im.putpixel((x, y), rgb)
				count = count + 1
		return im.copy()

	
		

class Steganography():

	def __init__(self, imagePath, direction = 'horizontal'):
		"""
		Instantiates a Steganography object based on scan direction and image to be used as steganomedium. Can handle only grayscale images as steganomedium.
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
		elif self.med.mode not in ['L']:
			raise TypeError('Not a Grayscale Image')
		else:	
			self.dir = direction
			self.eMed = None
			self.medSize = self.med.size[0] * self.med.size[1]
	
	def convertImagetoList(self, im):
		"""
		Converts an image to a list of pixel values using horizontal/vertical raster scan. If its a color image, the scan follows order, Red, then Green and then Blue channel 
		"""
		img = im.copy()
		if self.dir == 'horizontal':
			img = img
		else:
			img = img.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)
			
		if img.mode == 'L':
			return list(img.getdata(0))
		elif img.mode == 'RGB':	
		 	return list(img.getdata(0)) + list(img.getdata(1)) + list(img.getdata(2))
	
	def convertListToImage(self, i_list, img):
		"""
		Takes a list of pixel values and converts them into gray scale or color image based on image type
		"""
		im = img.copy()
		if self.dir == 'horizontal':
			im = im
		else:
			im = im.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM)

		w = im.size[0]
		h = im.size[1]
		if img.mode == 'L':
			count = 0
			for i in range(len(i_list)):
				x = count % w
				y = (count - x) / w
				im.putpixel((x, y), i_list[i])
				count = count + 1
		elif img.mode == 'RGB':
			count = 0
			for i in range(len(i_list)/3):
				x = count % w
				y = (count - x) / w
				rgb = (i_list[i], i_list[i + (1*w*h)], i_list[i + (2*w*h)])
				im.putpixel((x, y), rgb)
				count = count + 1
			
		if self.dir == 'horizontal':
			return im
		else:
			return im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
		
		
	def embedMessageInMedium(self, message, targetImagePath):
		"""
		Embeds the XML represtatin of the image into the specified Steganomedium image
		"""
		if (message.getMessageSize() * 8) > self.medSize:
			raise ValueError('Message Size greater than medium')
		else:
			im = self.med.copy()
			bin_str = self.convertToBin(message.getXmlString())
			im_data = self.convertImagetoList(im)
			
			for i in range(len(bin_str)):
				pv = im_data[i] % 2
				bv = int(bin_str[i])
				if pv == bv :
					value = im_data[i]
				elif pv == 1 and bv == 0:
					value = im_data[i] - 1
				elif pv == 0 and bv == 1:
					value = im_data[i] + 1

				im_data[i] = value


			im = self.convertListToImage(im_data, im)
			self.eMed = im
			try:
				im.save(targetImagePath)
			except KeyError:
				im.save(targetImagePath + '.png')
			except Exception as e:
				pass
		
	def convertToBin(self, xml_str):
		"""
		Converts a unicode character into its corresponding binary string representation 
		"""
		output = ""
		for x in xml_str:
			b = format(ord(x), 'b')
			b = b.zfill(8)
			output = output + b
		
		return output
	
	def extractMessageFromMedium(self):
		"""
		Extracts the XML representation of an image from the steganomedium. It then initaializes a Message object form the XML representation(using regex) filling in the required object members and returns the message object
		"""
		im_data = self.convertImagetoList(self.med)
		bin_str = ""
		for i in range(len(im_data)):
			pv = im_data[i] % 2
			bin_str = bin_str + str(pv)
		count = 0
		o_count = 0
		word = ""
		bin_list = []
		while o_count < len(bin_str):
			
			if count == 8:
				bin_list = bin_list + [word]
				word = ""
				count = 0
			else:
				word = word + bin_str[o_count]
				count = count + 1
				o_count = o_count + 1
		
		output = ""
		for b in bin_list:
			 output = output + chr(int(b, 2))
		
		r_str = r'^(<\?xml version="1.0" encoding="UTF-8"\?>\n)'
		r_str = r_str + r'<message type="(?P<mType>(GrayImage|ColorImage|Text))" size="(?P<size>(([0-9]+)|([0-9]+,[0-9]+)))" encrypted="(?P<enc>(False|True))">\n'
		r_str = r_str + r'(?P<msg>.*)\n'
		r_str = r_str + r'</message>' 
		
		if re.match(r_str, output):
			r = re.match(r_str, output)
			output = '<?xml version="1.0" encoding="UTF-8"?>\n'
			output = output + '<message type="%s" size="%s" encrypted="%s">\n'%(r.group('mType'), r.group('size'), r.group('enc'))
			output = output + r.group('msg') + '\n'
			output = output + '</message>'
			return Message(XmlString = output)
		else:
			return None
		
def main():
	
	ext = '.png'
	sourcePath = 'files/sunflower' + ext
        expectedPath = 'files/sunflower.xml'

        message = Message(filePath=sourcePath, messageType='ColorImage')
	"""
        with open('qwerty', 'w') as xmlFile:
            xmlString = message.getXmlString()
            xmlFile.write(xmlString)

        actualTextFile, expectedTextFile = loadTwoTextFiles('qwerty', expectedPath)

        print (actualTextFile == expectedTextFile)
	f = open('hello2', 'w')
	with open('files/full.xml', 'r') as g:
		f.write(g.read().replace('\r', ''))
	
	
	g = open('hello', 'w')
	m = Message(filePath = 'files/full.txt', messageType = 'Text')
	g.write(m.getXmlString())
	g.close()
		
	print m.getMessageSize()
	m.saveToTarget('qwerty')
	
	
	l = Message(filePath='files/dog.png', messageType='GrayImage')
	s = Steganography('files/bridge.png', direction = 'vertical')
	s.embedMessageInMedium(l, 'ns.png')
	#t = Steganography('bridgesecret.png', direction = 'horizontal')
	#a = t.extractMessageFromMedium()
	#print a.convertBase64ToUTF8(a.msgB64)	
	#with open('full.txt') as f:
	#	print f.read()
	
	m = Message(filePath='files/sunflower.png', messageType='ColorImage')
	m.getIMFromB64()
	m.saveToImage('dog2.png')
	a = list(Image.open('files/sunflower.png').getdata())
	b = list(Image.open('dog2.png').getdata())
	print (a == b)
	"""


if __name__ == "__main__":
	main()
