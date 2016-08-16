#! /usr/bin/env python
#
# $Author$
# $Date$
# $HeadURL$
# $Revision$

# Import PySide classes

import re
import sys
from PySide.QtCore import *
from PySide.QtGui import *
import EntryForm
import math

class SampleWindow(QMainWindow, EntryForm.Ui_MainWindow):

	def __init__(self, parent=None):
		super(SampleWindow, self).__init__(parent)
		self.setupUi(self)
		
		self.pbc.clicked.connect(self.handleClear)
		self.pbs.clicked.connect(self.handleSave)
		self.pbl.clicked.connect(self.handleLoad)
		self.pbc.setEnabled(True)		
		self.pbs.setEnabled(False)
		self.pbl.setEnabled(True)
		self.fn.textChanged.connect(self.handleChange)
		self.ln.textChanged.connect(self.handleChange)
		self.ad.textChanged.connect(self.handleChange)
		self.ct.textChanged.connect(self.handleChange)
		self.st.textChanged.connect(self.handleChange)
		self.zp.textChanged.connect(self.handleChange)
		self.em.textChanged.connect(self.handleChange)
		self.fn.setText(u'')
		self.ln.setText(u'')
		self.ad.setText(u'')
		self.ct.setText(u'')
		self.st.setText(u'')
		self.zp.setText(u'')
		self.em.setText(u'')
		self.errorLabel.setText(u'')
		self.stateCodes = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
    					"HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    					"MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    					"NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    					"SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
		
		
	def getData(self):
		fn = self.fn.text()
		ln = self.ln.text()
		ad = self.ad.text()
		ct = self.ct.text()
		st = self.st.text()
		zp = self.zp.text()
		em = self.em.text()
		return [fn, ln, ad, ct, st, zp, em]
	
	def readXML(self, lines):
		pat = r'^\t<FirstName>(?P<obj>.*)</FirstName>\n'
		fn = re.search(pat, lines[2]).group('obj')
		pat = r'^\t<LastName>(?P<obj>.*)</LastName>\n'
		ln = re.search(pat, lines[3]).group('obj')
		pat = r'^\t<Address>(?P<obj>.*)</Address>\n'
		ad = re.search(pat, lines[4]).group('obj')
		pat = r'^\t<City>(?P<obj>.*)</City>\n'
		ct = re.search(pat, lines[5]).group('obj')
		pat = r'^\t<State>(?P<obj>.*)</State>\n'
		st = re.search(pat, lines[6]).group('obj')
		pat = r'^\t<ZIP>(?P<obj>.*)</ZIP>\n'
		zp = re.search(pat, lines[7]).group('obj')
		pat = r'^\t<Email>(?P<obj>.*)</Email>\n'
		em = re.search(pat, lines[8]).group('obj')
		return [fn, ln, ad, ct, st, zp, em]
		
	def handleSave(self):
		data = self.getData()
		if data[0] == '':
			self.errorLabel.setText(u'Error: First Name cannot be empty.')
		elif data[1] == '': 
			self.errorLabel.setText(u'Error: Last Name cannot be empty.')
		elif data[2] == '': 
			self.errorLabel.setText(u'Error: Address cannot be empty.')
		elif data[3] == '': 
			self.errorLabel.setText(u'Error: City cannot be empty.')
		elif data[4] == '': 
			self.errorLabel.setText(u'Error: State cannot be empty.')
		elif data[5] == '':
			self.errorLabel.setText(u'Error: ZIP cannot be empty.')
		elif data[6] == '': 
			self.errorLabel.setText(u'Error: Email cannot be empty.')
		elif data[4] not in self.stateCodes:
			self.errorLabel.setText(u'Error: Invalid US State.')
		elif not re.match(r'^[0-9]{5}$', data[5]):
			self.errorLabel.setText(u'Error: Invalid ZIP Code.')
		elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data[6]):
			self.errorLabel.setText(u'Error: Invalid Email Address.')
		else:	
			self.errorLabel.setText(u'')
			fname = QFileDialog.getSaveFileName(self, 'Save File', '', '*.xml')
			file_contents = ['<?xml version="1.0" encoding="UTF-8"?>\n', 
			'<User>\n', 
			'\t<FirstName>%s</FirstName>\n'%(data[0]),
			'\t<LastName>%s</LastName>\n'%(data[1]), 
			'\t<Address>%s</Address>\n'%(data[2]), 
			'\t<City>%s</City>\n'%(data[3]), 
			'\t<State>%s</State>\n'%(data[4]), 
			'\t<ZIP>%s</ZIP>\n'%(data[5]), 
			'\t<Email>%s</Email>\n'%(data[6]), 
			'</user>\n']
			
			f = open(fname[0]+'.xml', 'w')
			for l in file_contents:
				f.write(l)
			f.close()
	def handleLoad(self):
		
		fname = QFileDialog.getOpenFileName(self, 'Open File', '.')
		f = open(fname[0], 'r')
		lines = f.readlines()
		data = self.readXML(lines)
		self.fn.setText(data[0])
		self.ln.setText(data[1])
		self.ad.setText(data[2])
		self.ct.setText(data[3])
		self.st.setText(data[4])
		self.zp.setText(data[5])
		self.em.setText(data[6])
		self.errorLabel.setText(u'')
		f.close()
		
	
	def handleChange(self):
		
		data = self.getData()
		flag = False
		for d in data:
			if d != u'':
				flag = True
		if flag == True: 
			self.pbc.setEnabled(True)		
			self.pbs.setEnabled(True)
			self.pbl.setEnabled(False)
		else:
			self.pbc.setEnabled(True)		
			self.pbs.setEnabled(False)
			self.pbl.setEnabled(True)
		

	def handleClear(self):
		self.pbc.setEnabled(True)		
		self.pbs.setEnabled(False)
		self.pbl.setEnabled(True)
		self.fn.textChanged.connect(self.handleChange)
		self.ln.textChanged.connect(self.handleChange)
		self.ad.textChanged.connect(self.handleChange)
		self.ct.textChanged.connect(self.handleChange)
		self.st.textChanged.connect(self.handleChange)
		self.zp.textChanged.connect(self.handleChange)
		self.em.textChanged.connect(self.handleChange)
		self.fn.setText(u'')
		self.ln.setText(u'')
		self.ad.setText(u'')
		self.ct.setText(u'')
		self.st.setText(u'')
		self.zp.setText(u'')
		self.em.setText(u'')
		self.errorLabel.setText(u'')	
			
		
	
			

				
def main():
	currentApp = QApplication(sys.argv)
	currentForm = SampleWindow()
	currentForm.show()
	currentApp.exec_()
	
if __name__ == '__main__':
	main()
