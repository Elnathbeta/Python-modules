#!/usr/bin/env python3
# coding=utf-8
# Watchdog for a configuration file.
# Reloads the configuration from the file when the file is changed
#
# Copyright (C) 2017 Elnath < elnathbeta@gmail.com >
#
# Licensed under the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of (the) Author shall not be used in advertising or
# otherwise to promote the sale, use or other dealings in this Software without
# prior written authorization from (the)Author.

import sys
import json
import os.path

try:
	import watchdog.observers, watchdog.events
except ImportError as e:
	sys.stderr.write("****\nDependency watchdog not available! Did you run 'pip install -r requirements.txt'?\n****\n")
	raise e


class ConfigWatchdog(watchdog.events.FileSystemEventHandler):
	"""
	A class used to reload a json config file every time it is changed on disk.
	The object will always have the latest values of the config.
	If the config file is deleted, the config will be empty.

	This objects emulates all functions of container-type objects, so you can use it like a dict or list
	(depending on how your config file is written). These calls will just be passed to the underlying `config` attribute.
	You can set values for config, but beware that everything will be overridden when the file changes.
	"""

	def __init__(self, configfilename: str, autostart = True, logger = None):
		"""
		:param configfilename: The name of the config file to watch
		:param autostart: Whether to start watching the file as soon as the object is constructed
		:param logger: (optional) A logger to which we will log events. It can be any object with a .info(message) and
			.error(message) methods.
		"""
		self.config = {}
		self._configFilename = os.path.abspath(configfilename)
		self._logger = logger
		self._observer = watchdog.observers.Observer()
		self._observer.schedule(self, os.path.abspath(
			os.path.dirname(configfilename)))  # We set ourselves as the event handler
		if autostart:
			self.start()

	def start(self):
		"""
		Start watching the config file for changes
		"""
		self._observer.start()
		if self._logger is not None:
			self._logger.info("Started watching for config changes")
		# We load the initial config
		self._reloadConfig()

	def stop(self):
		"""
		Stop watching for changes
		"""
		self._observer.stop()
		if self._logger is not None:
			self._logger.info("Stopped watching for config changes")

	# **** Emulating a container type ****
	def __getitem__(self, item):
		return self.config[item]

	def __contains__(self, item):
		return self.config.__contains__(item)

	def __len__(self):
		return self.config.__len__()

	def __setitem__(self, key, value):
		return self.config.__setitem__(key, value)

	def __delitem__(self, key):
		return self.config.__delitem__(key)

	def __iter__(self):
		return self.config.__iter__()

	def __reversed__(self):
		return self.config.__reversed__()

	def _reloadConfig(self):
		if os.path.isfile(self._configFilename):
			try:
				with open(self._configFilename, "r") as configFile:
					self.config = json.load(configFile)
			except (OSError, ValueError) as e:
				# We do not modify the current config
				if self._logger is not None:
					self._logger.error("Config loading aborted: error when loading config: %s " % e)
		else:
			self.config.clear()
			if self._logger is not None:
				self._logger.info("Config file doesn't exist")

	# ***** Overriding base class handlers *****
	def on_created(self, event):
		if event.src_path != self._configFilename:
			return
		if self._logger is not None:
			self._logger.info("Config file created")
		self._reloadConfig()

	def on_deleted(self, event):
		if event.src_path != self._configFilename:
			return
		if self._logger is not None:
			self._logger.info("Config file deleted. Emptying config")
		self.config.clear()

	def on_modified(self, event):
		if event.src_path != self._configFilename:
			return
		if self._logger is not None:
			self._logger.info("Config file modified. Reloading config")
		self._reloadConfig()

	def on_moved(self, event):
		# The config file can be either the source or the destination of the move
		if (event.src_path == self._configFilename) or (event.dest_path == self._configFilename):
			if self._logger is not None:
				self._logger.info("Config file moved. Reloading config")
			self._reloadConfig()
