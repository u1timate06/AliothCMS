#!/usr/bin/env python
# __Author__:cmustard

import logging
import os

from util.config import *


def printInfo(file,message):
	"""
	格式化打印错误信息
	:param file: __file__
	:param message:  e
	:return:
	"""
	return "An error occurred in file {},  error is {}".format(os.path.basename(file),message)



def getLogger():
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
	if Debug:
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

def calcProbability(rawData):
	"""
	计算概率
	:param rawData:{"Hawei":2,"h3c":3,"kk":1}
	:return:
	"""
	logger = getLogger()
	total = 0
	probabilDict = dict()
	for key,value in rawData.items():
		try:
			total = int(value)+total
		except Exception as e:
			logger.error(printInfo(__file__,str(e)+",function is calcProbability"))
			continue
	for key in rawData.keys():
		try:
			probabilDict[key] = "{:.2f}%".format(rawData[key]/float(total)*100)
		except Exception as e:
			logger.error(printInfo(__file__,str(e)+", function is calcProbability"))

	return probabilDict


if __name__ == '__main__':
	data = {"Hawei":2,"h3c":"qq","kk":1}
	print(calcProbability(data))