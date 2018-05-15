#!/usr/bin/env python
# __Author__:cmustard

import logging
import os

from util.config import *


def printInfo(file,message):
	"""

	:param file: __file__
	:param message:  e
	:return:
	"""
	return "An error occurred in file {},  error is {}".format(os.path.basename(file),message)



def getLogger(isDebug=False):
	"""
	log handler
	:param isDebug:
	:return: logger
	"""
	logger = logging.Logger("cms")
	formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
	path = LOGFILE
	fh = fileHandler(path,formatter)
	sh = streamHandler(formatter)
	if isDebug:
		logger.setLevel(logging.DEBUG)
	logger.addHandler(fh)
	logger.addHandler(sh)
	return logger


def fileHandler(path,formatter):
	"""
	log file
	:param path:
	:return: handler
	"""
	fh = logging.FileHandler(path)
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	return fh

def streamHandler(formatter):
	"""

	:return: handler
	"""
	sh = logging.StreamHandler()
	sh.setLevel(logging.ERROR)
	sh.setFormatter(formatter)
	return sh