#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	MaxLevelFilter. This file defines a class that is meant to be used with the logging module.
	This filter block everything that has a priority higher than the priority passed to its constructor.
	If you want for example to redirect INFO and DEBUG to stdout and WARNING and higher to stderr, this is the
	module you're looking for!
	
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
import logging

class MaxLevelFilter():
	"""
		Allows only messages with level < Level attribute.
		Note that it is 'strictly inferior', because logger.setLevel is inclusive.
	"""
	def __init__(self, level):
		self.Level = level
	
	def filter(self, record):
		"""
			Process the event.
			:return: True if the event should be logged, False otherwise
		"""
		return record.levelno < self.Level
	
#EXAMPLE: We want to log every INFO and DEBUG message to stdout and other messages to stderr
if __name__ == "__main__":
	import sys
	
	LOGGER = logging.getLogger(__name__)
	LOGGER.setLevel(logging.DEBUG) #We will log every message
	stdout_hdlr = logging.StreamHandler(sys.stdout)
	stdout_hdlr.addFilter(MaxLevelFilter(logging.WARNING)) #Note: WARNING messages won't go in there
	LOGGER.addHandler(stdout_hdlr)
	stderr_hdlr = logging.StreamHandler(sys.stderr)
	stderr_hdlr.setLevel(logging.WARNING) #Note: WARNING messages will go in there
	LOGGER.addHandler(stderr_hdlr)
	
	#Now, some messages
	LOGGER.debug("This is a DEBUG message and will go to stdout")
	LOGGER.error("This is an ERROR message and will go to stderr")
	LOGGER.warning("This is a WARNING message and will also go to stderr")