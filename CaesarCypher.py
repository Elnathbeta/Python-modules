#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	CaesarCypher.py
	This module implements simple writing and reading methods for files based on the Caesar cypher.
	It's a quite simple encryption method: every character is converted to its numerical value, a value is added to it and then it is reconverted to a character and printed to the file.
	It is not meant to be sure or really good, it only outputs a file that is not human-readable. Output file is encoded in utf-8 (just for info).
	Objects support the with statement.
	See the end of the module for examples.
	
	This module is distributed under the MIT License
	
	Copyright (c) 2014 Glenderin/Elnath
	Version of July 2014, Revision of July 2015
	
	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:
	
	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.
	
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.
	
	Except as contained in this notice, the name(s) of (the) Author shall not be used in advertising or 
	otherwise to promote the sale, use or other dealings in this Software without 
	prior written authorization from (the )Author.
"""

import codecs
import random

class CaesarWriter():
	def __init__(self, filename, offset = None):
		"""
			Creates an object used to write the encrypted file.
			*filename (string): the name of the file that will be written.
			*offset (int): the number that is added to the value of every character. Must be between 0 and 255. If None, a random number is generated.
			
			You can access the file opened by this object with his file attribute (but it is not recommended).
			The offset value is stored in the offset attribute
			Don't forget to close the object at the end. Or you can use a with statement, that's better.
			It supports the with statement.
			
			How it works:
			A file is created with codecs.open(filename, "wb", encoding = "utf-8"), the first character written to the file is the offset(so we can read it later).
			When you use the write method, every character is converted to its numeric value, offset is added, and then it is converted to the character value and written to the file.
		"""
		if offset == None:
			offset = random.randint(1, 254) #We don't include 0 and 255, because that will mean characters are not converted so the file is human-readable.
		elif not isinstance(offset, int): #offset is passed: we verify if it is a integer
			try:
				offset = int(offset)
			except ValueError:
				raise TypeError("Offset must be a int, castable to int or None")
		if offset < 0:
			offset = -offset
		if offset > 255:
			raise ValueError("Offset must be between 0 and 255")
		self.offset = offset
		
		if isinstance(filename, str):
			self.file = codecs.open(filename, "wb", encoding = "utf-8")
		else:
			raise TypeError("Filename must be a string")
		
		self.file.write(unichr(self.offset)) #The first char in the file will be the offset so we can retrieve it when we read the file
	
	def write(self, text):
		"""Writes some text to the file"""
		if not isinstance(text, str):
			text = str(text)
		for c in text:
			x = (ord(c) + self.offset) % 255 #If > 255, then it will be its value-255 
			self.file.write(unichr(x))
	
	def writelines(self, lines):
		"""Writes multiple lines to the file."""
		for element in lines:
			self.write(element)
	
	def close(self):
		"""Close the file attached to the object. """
		self.file.close()
		
	def __enter__(writer):
		return writer
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

class CaesarReader():
	def __init__(self, filename):
		"""
			Creates an object used to read the encrypted file.
			*filename (string): the name of the file to open.
			
			Returns unicode encoded strings.
			You can access the file opened by this object with his file attribute (but it is not recommended).
			You can access the offset with the offset attribute.
			Don't forget to close the object at the end. Or you can use a with statement, that's better
			It supports the with statement.
		"""
		if isinstance(filename, str):
			self.file = codecs.open(filename, "rb", encoding = "utf-8")
		else:
			raise TypeError("Filename argument must be a string")
			
		self.offset = ord(self.file.read(1)) #The first char in the file is the offset
	
	def read(self, size = None):
		"""Reads size bytes from the file"""
		result = ""
		buffer = self.file.read(size)
		for c in buffer:
			x = ord(c) - self.offset
			if x <= 0:
				x = x+255
			result += chr(x)
		return result
	
	def readline(self):
		"""Reads from the file till a line break or EOF is found"""
		result = ""
		readloop = True
		while readloop:
			c = self.read(1)
			result += c
			if c == "": #This is the End of the file
				readloop = False
			if c == "\n":
				readloop = False
		return result
	
	def readlines(self):
		result = []
		readloop = True
		while readloop:
			line = self.readline()
			if line == "":
				readloop = False
			else:
				result.append(line)
		return result
	
	def close(self):
		"""Close the file attached to the object."""
		self.file.close()
	
	def __enter__(writer):
		return writer
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.file.close()
		
def encrypt(origin_file, end_file, offset):
	"""Write the encrypted content of origin_file to end_file"""
	with open(origin_file, "r") as reader:
		with CaesarWriter(end_file, offset) as writer:
			for line in reader.readlines():
				writer.write(line)
def decrypt(origin_file, end_file):
	"""Write the decrypted content of origin_file(must have been previously encrypted by this module) to end_file"""
	with CaesarReader(origin_file) as reader:
		with open(end_file, "w") as writer:
			for line in reader.readlines():
				writer.write(line)

#EXAMPLE
		
if __name__ == "__main__":
	print("This module will print a test file")
	name = raw_input("Enter the name of the file: ")
	# name = "test.txt"
	with CaesarWriter(name, 0) as out:
		out.write("First line\n")
		out.write("This is the second line")
		out.write(" This is also the second line")
		out.write("\nA third line because why not? And somê sp€ciàl ch@rs§")
	with CaesarReader(name) as reader:
		print "Content of the file when decrypted:"
		for line in reader.readlines():
			print line
