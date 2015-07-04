#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
	randomname. This module defines some useful(I hope) functions for giving files a random name.
	There are two types of function: the ones that start with a r give names with lowercase letters and digits,
	the ones that start with a d give names with only digits.
	You can generate a random name, rename a file, or even rename an entire directory or directory tree.
	
	This module is distributed under the MIT License
	
	Copyright (c) 2015 Elnath < elnathbeta@gmail.com >

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

import random
import os

def rname(namelength = 15):
	"""
		Generates a random name. The name will be namelength long and will contain
		lowercase letters and digits.
	"""
	result = ""
	for x in range(namelength):
		result += random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
	return result

def dname(namelength = 15):
	"""
		Generates a digit-only random name. The name will be namelength long and will only contain digits.
	"""
	result = ""
	for x in range(namelength):
		result += random.choice("0123456789")
	return result
	
def rrename(filepath, namelength = 15):
	"""
		Rename the file filepath with a random name. The name will be namelength long.
	"""
	filepath = os.path.abspath(filepath)
	if not os.path.isfile(filepath):
		raise ValueError("The path is not a valid file path: "+str(filepath))
	
	path, name = os.path.split(filepath)
	name, ext = os.path.splitext(name)
	os.rename(filepath, os.path.join(path, rname(namelength)+ext)) #We replace name by the random name and reconstruct the path

def drename(filepath, namelength = 15):
	"""
		Same as rrename, but with digit-only names.
	"""
	filepath = os.path.abspath(filepath)
	if not os.path.isfile(filepath):
		raise ValueError("The path is not a valid file path: "+str(filepath))
	
	path, name = os.path.split(filepath)
	name, ext = os.path.splitext(name)
	os.rename(filepath, os.path.join(path, dname(namelength)+ext)) #We replace name by the random name and reconstruct the path
	
def rrenameall(folderpath = None, namelength = 15, recursive = False):
	"""
		Rename all files in folderpath folder.
		If folderpath is None, the os.getcwd() is used.
		If recursive is True, then all files in subfolders are also renamed.
		Folders are not renamed!
		Doesn't follow symlinks (may lead to infinite loop).
	"""
	if folderpath == None:
		folderpath = os.getcwd()
	else:
		folderpath = os.path.abspath(folderpath)
		if not os.path.isdir(folderpath):
			raise ValueError("The path is not a valid folder path: "+str(folderpath))
	
	if recursive:
		def onerror(error):
			print "There was an error with a directory: "+str(error)
			
		for (dirpath, dirnames, filenames) in os.walk(folderpath, onerror = onerror):
			for name in filenames:
				rrename(os.path.join(dirpath, name), namelength)
	else:
		for name in os.listdir(folderpath):
			filepath = os.path.join(folderpath, name)
			if os.path.isfile(filepath):
				rrename(filepath, namelength)
			
def drenameall(folderpath = None, namelength = 15, recursive = False):
	"""
		Same as rrenameall, but with digit-only names.
	"""
	if folderpath == None:
		folderpath = os.getcwd()
	else:
		folderpath = os.path.abspath(folderpath)
		if not os.path.isdir(folderpath):
			raise ValueError("The path is not a valid folder path: "+str(folderpath))
	
	if recursive:
		def onerror(error):
			print "There was an error with a directory: "+str(error)
			
		for (dirpath, dirnames, filenames) in os.walk(folderpath, onerror = onerror):
			for name in filenames:
				drename(os.path.join(dirpath, name), namelength)
	else:
		for name in os.listdir(folderpath):
			filepath = os.path.join(folderpath, name)
			if os.path.isfile(filepath):
				drename(filepath, namelength)
	