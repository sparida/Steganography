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
import sys
import glob
from Crypto.Cipher import AES
from PIL import Image
from PIL import ImageQt
from os.path import join
from os.path import split
import re
from PySide.QtCore import *
from PySide.QtGui import *
import SteganographyGUI

from NewSteganography import NewSteganography
from ExtendedSteganography import AesMessage

class SampleWindow(QMainWindow,SteganographyGUI.Ui_MainWindow):

	def __init__(self, parent=None):
		"""
		Initializes folder selection dialog, and if valid folder is selected,initializes GUI with image list
		"""
		self.msg_list = []
		self.msg_type = []
		self.no_msg_list = []
		self.fname = None
		self.sel_name = None
		self.cur_msg_type = None
		super(SampleWindow, self).__init__(parent)
		self.setupFlag = False
		self.fname = QFileDialog.getExistingDirectory(self, 'Choose A Folder')
		self.checkValidFolderName()	
		self.initGUI()
	
	def initGUI(self):
		"""
		If folder selection is valid initializes GUI with populated image list 
		"""
		if self.setupFlag == True:		
			self.setupUi(self)
			self.setMedia()
			self.btnExtract.clicked.connect(self.handleExtract)
			self.btnWipeMedium.clicked.connect(self.handleWipe)
			self.show()
		else:
			exit(0)

	def checkValidFolderName(self):
		"""
		Checks if folder selection is valid or not 
		"""
		if len(self.fname) != 0:
			self.setupFlag = True
	
	def getImageFilesList(self):	
		"""
		Gets list of all images in the current folder
		"""
		types = ('*.png', '*.jpg', '*.tif', '*.bmp', '*.gif') # the tuple of file types
		files_list = []
		for t in types:
			files_list.extend(glob.glob(join(self.fname, t)))
		return files_list
	
	def setMedia(self):
		"""
		Takes list of all image sin folder and populates tree widget in GUI according to whtehr they have messages or not and their respective message type, i.e. initial state of GUI
		"""
		self.fileTreeWidget.clear()
		f_list = self.getImageFilesList()
		self.msg_list = []
		self.msg_type = []
		self.no_msg_list = []
		dummy_sel = ""
		for f in f_list:
			nh = NewSteganography(f, direction = 'horizontal')
			nv = NewSteganography(f, direction = 'vertical')
			ah, bh = nh.checkIfMessageExists()
			av, bv = nv.checkIfMessageExists()
			if ah != av:
				self.msg_list = self.msg_list + [split(f)[-1]]
				if ah == True:
					self.msg_type = self.msg_type + [bh]
				else:
					self.msg_type = self.msg_type + [bv]
			else: 
				self.no_msg_list = self.no_msg_list + [split(f)[-1]]
			
		l = []  # list of QTreeWidgetItem to add
		fontnm = QFont()
		fontnm.setBold(False)
		fontnm.setPointSize(8)
		brushnm = QBrush()
		brushnm.setColor('blue')
		fontm = QFont()
		fontm.setBold(True)
		fontm.setPointSize(8)
		brushm = QBrush()
		brushm.setColor('red')
		fontmt = QFont()
		fontmt.setBold(False)
		fontmt.setPointSize(8)
		brushmt = QBrush()
		brushmt.setColor('green')

		for i in range(len(self.no_msg_list)):
			a = QTreeWidgetItem()
			a.setText(0, self.no_msg_list[i])
			a.setFont(0, fontnm)
			a.setForeground(0, brushnm)
    			l = l + [a]
			if self.no_msg_list[i] == self.sel_name:
				dummy_sel = a
		
		for i in range(len(self.msg_list)):
			a = QTreeWidgetItem()
			a.setText(0, self.msg_list[i])
			a.setFont(0, fontm)
			a.setForeground(0, brushm)
			c = QTreeWidgetItem()
			c.setText(0, self.msg_type[i])
			c.setFont(0, fontmt)
			c.setForeground(0, brushmt)
			a.addChild(c)
			l = l + [a]
		
		self.fileTreeWidget.addTopLevelItems(l)
		for i in l:
			self.fileTreeWidget.expandItem(i)
		
		self.fileTreeWidget.itemClicked.connect(self.handleSelection)
		self.cur_msg_type = None
		self.grpMedium.setEnabled(True)
		self.grpMessage.setEnabled(True)
		self.viewMedium.setEnabled(False)
		self.btnExtract.setEnabled(False)
		self.btnWipeMedium.setEnabled(False)
		self.stackMessage.setCurrentWidget(self.pgText)
		self.stackMessage.setEnabled(False)
		self.txtMessage.setEnabled(False)
		self.viewMessage.setEnabled(False)

		if isinstance(dummy_sel, QTreeWidgetItem):
			self.fileTreeWidget.setCurrentItem(dummy_sel)
			

	def handleSelection(self, item, column):
		"""
		Handles selection of the TreeWidget. Calls appropriate display function based on whether selection contains message or not and correct message type
		"""
		sel_name = item.text(column)
		if sel_name in ['GrayImage', 'ColorImage', 'Text']:
			self.sel_name = sel_name
		elif sel_name in self.no_msg_list:
			self.displayMediumNoMessage(sel_name)
			self.sel_name = sel_name
		elif sel_name in self.msg_list:
			self.displayMediumWithMessage(sel_name)
			self.sel_name = sel_name
	
	def displayMediumWithMessage(self, sel_name):
		"""
		Setups GUI to display a medium which contains a message, according to specifications. Message section is enable dwith appropriate message type
		"""
		self.cur_msg_type = None
		self.grpFiles.setEnabled(True)
		self.grpMedium.setEnabled(True)
		self.btnExtract.setEnabled(True)
		self.btnWipeMedium.setEnabled(True)
		self.grpMessage.setEnabled(True)
		self.stackMessage.setEnabled(True)
		self.txtMessage.setEnabled(True)
		self.viewMessage.setEnabled(True)

		self.cur_msg_type = self.msg_type[self.msg_list.index(sel_name)]
		if self.cur_msg_type == "Text":
			self.stackMessage.setCurrentWidget(self.pgText)
			self.pgText.setEnabled(True)
			self.txtMessage.clear()
			self.txtMessage.setReadOnly(True)


			
		else:
			self.stackMessage.setCurrentWidget(self.pgImage)
			self.pgImage.setEnabled(True)
			scn = QGraphicsScene()
			scn.clear()
			self.viewMessage.setScene(scn)
			self.viewMessage.show()

			
		Qim = QImage(join(self.fname, sel_name))
            	pixmap = QPixmap.fromImage(Qim)
		pixItem = QGraphicsPixmapItem(pixmap)
		scn = QGraphicsScene()
		self.viewMedium.setScene(scn)
		scn.addItem(pixItem)
		self.viewMedium.fitInView(pixItem)
		self.viewMedium.show()
	
	def handleExtract(self):
		"""
		Handle the extract button clicked event. Extracts message and displays it in message section. Asks for password if message in encrypted
		"""
		if self.cur_msg_type == "Text":
			med_path = join(self.fname, self.sel_name)
			nh = NewSteganography(med_path, direction = 'horizontal')
			nv = NewSteganography(med_path, direction = 'vertical')
			ah, bh = nh.checkIfMessageExists()
			if ah == True:
				m = nh.extractMessageFromMedium()
			else:
				m = nv.extractMessageFromMedium()
			if m.isEncrypted == "True":
				text, ok = QInputDialog().getText(self, 'Password', 'Enter password:', echo=QLineEdit.Password)	
				
              			if ok and (len(text) == 16):
					em = AesMessage(m, text)
					ok_flag = self.isPasswordLegal(em.msgStr)
					if ok_flag:
						self.txtMessage.setPlainText(em.msgStr)
						self.btnExtract.setEnabled(False)
					else:
						flags = QMessageBox.StandardButton.Ok
						msg = "Wrong Password!"
						response = QMessageBox.warning(self, "Error!", msg, flags)
						self.btnExtract.setEnabled(True)
				else:
					flags = QMessageBox.StandardButton.Ok
					msg = "Wrong Password!"
					response = QMessageBox.warning(self, "Error!", msg, flags)
					self.btnExtract.setEnabled(True)
			else:
				self.txtMessage.setPlainText(m.msgStr)
				self.btnExtract.setEnabled(False)		
		else:
			med_path = join(self.fname, self.sel_name)
			nh = NewSteganography(med_path, direction = 'horizontal')
			nv = NewSteganography(med_path, direction = 'vertical')
			ah, bh = nh.checkIfMessageExists()
			if ah == True:
				m = nh.extractMessageFromMedium()
			else:
				m = nv.extractMessageFromMedium()
					
			if m.isEncrypted == "True":
				text, ok = QInputDialog().getText(self, 'Password', 'Enter password:', echo=QLineEdit.Password)
              			if ok:
					em = AesMessage(m, text)
					em.saveToTarget('dummy.png')
					self.handleDisplayMessage()
					self.btnExtract.setEnabled(False)
			else:
				m.saveToTarget('dummy.png')
				self.handleDisplayMessage()
				self.btnExtract.setEnabled(False)

	
	def isPasswordLegal(self, text):
		"""
		Checks if password passed produces legal ascii characters and hence if the password is legal or not
		"""
		ret_val = False
		if all([(ord(c) < 128) for c in text]) == True:
			ret_val = True
		return ret_val
	
	def handleDisplayMessage(self):
		"""
		"""
		Qim = QImage('dummy.png')
            	pixmap = QPixmap.fromImage(Qim)
		pixItem = QGraphicsPixmapItem(pixmap)
		scn = QGraphicsScene()
		self.viewMessage.setScene(scn)
		scn.addItem(pixItem)
		self.viewMessage.fitInView(pixItem)
		self.viewMessage.show()
		

	def handleWipe(self):
		"""
		Handles Wipe Button Click. Asks if user is sure to wipe medium or not and proceeds only if user confirms. The Tree Widget is reset to include wiped image and te message section is disabled
		"""
		reply = QMessageBox.question(self, 'Warning', "Are you sure you want to proceed wiping (irreversible action) the medium?",      							QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        	if reply == QMessageBox.Yes:
			med_path = join(self.fname, self.sel_name)
			n = NewSteganography(med_path)
			n.wipeMedium()
			self.txtMessage.clear()
			self.setMedia()
			
			#self.displayMediumNoMessage(self.sel_name)
	
	def displayMediumNoMessage(self, sel_name):
		"""
		Setups GUI to display a medium which does not contain a message, according to specifications. Message section is disabled
		"""
		self.sel_name = sel_name
		self.cur_msg_type = None
		self.grpFiles.setEnabled(True)
		self.grpMedium.setEnabled(True)
		self.grpMessage.setEnabled(True)
		self.viewMedium.setEnabled(True)
		self.btnExtract.setEnabled(False)
		self.btnWipeMedium.setEnabled(False)
		self.stackMessage.setEnabled(False)
		#im = Image.open(join(self.fname, sel_name))
		#Qim = self.convertToQt(im)
		Qim = QImage(join(self.fname, sel_name))
            	pixmap = QPixmap.fromImage(Qim)
		pixItem = QGraphicsPixmapItem(pixmap)
		scn = QGraphicsScene()
		self.viewMedium.setScene(scn)
		scn.addItem(pixItem)
		self.viewMedium.fitInView(pixItem)
		self.viewMedium.show()
		self.txtMessage.clear()
		self.stackMessage.setCurrentWidget(self.pgText)
		self.stackMessage.setEnabled(False)
		self.txtMessage.setEnabled(False)
		self.viewMessage.setEnabled(False)

	
	def convertToQt(self, im):
		"""
		Converts PIL image to QT Image
		"""
		data = None
		if im.mode == "L":
			form = QImage.Format_Indexed
			data = im.tobytes()
		elif im.mode == "RGB":
			data = im.tobytes("raw", "BGRX")
			form = QImage.Format_RGB32
		else:
			raise ValueError("unsupported image mode %r" % im.mode)
		
		return QImage(data, im.size[0], im.size[1], form)

	
def main():
	currentApp = QApplication(sys.argv)
	currentForm = SampleWindow()
	currentApp.exec_()
	
if __name__ == '__main__':
	main()

