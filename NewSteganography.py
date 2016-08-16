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
# PySide 1.2.2

import base64
from Crypto.Cipher import AES
from PIL import Image
import re
from Steganography import Message, Steganography
from ExtendedSteganography import AesMessage

class NewSteganography(Steganography):
	def __init__(self, imagePath, direction='horizontal'):
		
		"""
		Instantiates a NewSteganography object based on embed direction and image to be used as steganomedium. Can handle both grayscale and color images as steganomedium. All other functions are inherited from Steganography class in Steganography.py
		"""	
		import base64
		from PIL import Image
		from Crypto.Cipher import AES
		import re
		from Steganography import Message, Steganography
		from ExtendedSteganography import AesMessage

		self.containsMsg = False
		try:
			self.med = Image.open(imagePath)
			self.imPath = imagePath
		except:
			raise ValueError('Invalid File Name')
		if direction not in ['horizontal', 'vertical']:
			raise ValueError('Unknown Direction.')
		elif self.med.mode not in ['RGB', 'L']:
			raise TypeError('Not a Color Image')
		else:	
			self.dir = direction
			self.eMed = None
			if self.med.mode == 'L':
				self.medSize = self.med.size[0] * self.med.size[1]
			elif self.med.mode == 'RGB':
				self.medSize = self.med.size[0] * self.med.size[1] * 3
			#self.containsMsg = self.checkIfMessageExists()

	def wipeMedium(self):
		"""
		Wipes medium clear off any message and stores it in original location
		"""
		im = self.med.copy()
		im_data = self.convertImagetoList(im)
		for i in range(len(im_data)):
			pv = im_data[i] % 2
			if pv == 0 :
				value = im_data[i]
			elif pv == 1:
				value = im_data[i] - 1
			im_data[i] = value

		im = self.convertListToImage(im_data, im)
		self.eMed = im
		try:
			im.save(self.imPath)
		except Exception as e:
			pass
	
	def checkIfMessageExists(self):
		"""
		Checks if given medium has an embedded message or not. Return True/False along with ,MessageType/None
		"""
		im_data = self.convertImagetoList(self.med)
		bin_str = ""
		for i in range(1000):
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
		r_str = r_str + r'<message type="(?P<mType>(GrayImage|ColorImage|Text))" size="(?P<size>(([0-9]+)|([0-9]+,[0-9]+)))" encrypted="(?P<enc>(False|True))">\n.*'
		
		if re.match(r_str, output):
			r = re.match(r_str, output)
			return (True, r.group('mType'))
		else:
			return (False, None)

def main():
	n = NewSteganography('files/lena.png')
	print n.checkIfMessageExists()

if __name__ == '__main__':
	main()

