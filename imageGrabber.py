#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
	Base script for grabbing images from internet pages.
	Analyses a page and extract information about the image(s) to download and download them.
	Modify pageParser class to customize the analysis.
"""

import logging
import os
import sys
import urllib2
import HTMLParser

# OPTIONS
OPTIONS = {
	"url": "", #The url of the page to analyse 
	"downloadDir": os.path.join(os.getcwd(), "out"), #Files will be downloaded in this folder
	"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36" #User agent that will be sent to the server, so it doesn't know that the request come from a script
}

#SETTING UP LOGGING
logformat = "=>%(asctime)s [%(levelname)s] %(message)s" #Add %(threadName)s for the name of the tread that logged the message

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter(logformat))
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(logging.Formatter(logformat))
#Splitting between err and out based on levels
class MaxLevelFilter():
	"""
		Allows only messages with level < Level attribute. Note that it is 'strictly lower', because logger.setLevel is inclusive.
	"""
	def __init__(self, level):
		self.Level = level
	def filter(self, record):
		"""
			Process the event.
			:return: True if the event should be logged, False otherwise
		"""
		return record.levelno < self.Level
stdout_handler.addFilter(MaxLevelFilter(logging.WARNING))
stderr_handler.setLevel(logging.WARNING)
LOGGER.addHandler(stdout_handler)
LOGGER.addHandler(stderr_handler)

class PageParser(HTMLParser.HTMLParser):
	"""
		This class will parse a HTML page and search for the image url.
		The feed method will launch the parsing (and return the result)
	"""
	def feed(self, HTML):
		"""
			Parse the HTML content passed as parameter.
			This method calls the feed method of HTMLParser.HTMLParser, but it will also return a result.
			Returns a tuple ([imageDirectUrls]) by default, you can extend it to add other vars to the tuple
		"""
		self.imageUrls = [] #A list of URLs that are direct link to the images. This will be used to download them
		HTMLParser.HTMLParser.feed(self, HTML) #Parsing. This will call other methods of this class
		return (self.imageUrls, ) # (The comma at the end will make sure we create a tuple)
	
	def handle_starttag(self, tag, attrs):
		"""
			This method is called when an opening tag is found in the HTML.
			For example, if <a href="http://test"> is found this method will be called with tag="a" and attrs=[("href", "http://test")]
		"""
		if tag == "img":
			attrnames = [element[0] for element in attrs]
			if "src" in attrnames: #"If the image has an attribute src
				self.imageUrls.append(attrs[attrnames.index("src")][1]) #Adding the second element of the attribute "src" (this will be the link)
	
	def handle_data(self, data):
		"""
			This method is called for data inside a tag.
			For example, if <div>test</div> is found this method will be called with data="test"
		"""
		pass
		
	def handle_endtag(self, tag):
		"""
			This method is called when an ending tag is found.
			For example, if </a> is found this method will be called with tag="a"
		"""
		pass
	
def urlopen(url, data = None, **additionalHeaders):
	"""
		Open a connectio to a page. This will create a urllib2.Request for url that contains an User-agent, so the site won't know that we are running a script.
		:param url: The url of the request
		:param data: Data that will be sent to the server as a POST request. If None, GET method is used instead
		:param additionalHeaders: Headers that will be added to the request. The User-agent is always added
		:return: the opened url. You can call read() on that object to read the HTML code
	"""
	txtheaders = {"User-agent": OPTIONS["user-agent"]}
	txtheaders.update(additionalHeaders)
	request = urllib2.Request(url, data, txtheaders)
	return urllib2.urlopen(request)

# CREATING OUTPUT DIR
if not os.path.isdir(OPTIONS["downloadDir"]):
	try:
		LOGGER.info("Download directory not found. Making it...")
		os.makedirs(OPTIONS["downloadDir"])
	except OSError as e:
		LOGGER.critical("Error: can't create download directory: "+str(e))
		sys.exit(1)
	
try:
	LOGGER.debug("Opening url: "+OPTIONS["url"])
	page = urlopen(OPTIONS["url"])
	parser = PageParser()
	LOGGER.info("Parsing page...")
	images = parser.feed(page.read())[0]
	
	for i in range(len(images)):
		LOGGER.info("Downloading "+str(images[i]))
		with open(os.path.join(OPTIONS["downloadDir"], str(i)+os.path.splitext(images[i])[1]), "wb") as imgfile:
			img = urlopen(images[i])
			imgfile.write(img.read())
except urllib2.HTTPError as e:
		LOGGER.critical("HTTP Error in fetching url: "+str(e))
		sys.exit(1)
except urllib2.URLError as e:
	LOGGER.critical("Connection error in fetching url: "+str(e))
	sys.exit(1)
except HTMLParser.HTMLParseError as e:
	LOGGER.critical("HTML parse error: "+str(e))
	sys.exit(1)
except (OSError, IOError) as e:
	LOGGER.critical("Error with file creation/download: "+str(e))
	sys.exit(1)
except ValueError as e:
	LOGGER.critical("ValueError: "+str(e))
	sys.exit(1)