# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-08 17:40:30
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-08 19:13:05

import glob
import datetime
import os
import pandas
import urllib
import subprocess
from selenium import webdriver
import selenium

from auto_settings import settings

# Provide strings to represent path to file and parsing instructions
fileSearchString = "\\\\bos-mart.ip-tech.com\\FSNPublishedReports\\ITDevelopment\\Petsmart_Backstop_*"
strpFormatString = "\\\\bos-mart.ip-tech.com\\FSNPublishedReports\\ITDevelopment\\Petsmart_Backstop_%m-%d-%Y_at_%H.%M.xlsx"

home_dir = os.path.expanduser('~')
vixxoUploadDirectory = os.path.join(home_dir, 'surveyMagic')
if not os.path.exists(vixxoUploadDirectory):
	os.makedirs(vixxoUploadDirectory)

def getNewestFile():
	#This will return a list of dicts, basically like
	#using csv.DictReader to read into a list.
	matchingFiles = glob.glob(fileSearchString)

	newestFile = matchingFiles[0]
	for eachfile in matchingFiles:
		if datetime.datetime.strptime(eachfile, strpFormatString) > datetime.datetime.strptime(newestFile, strpFormatString):
			newestFile = eachfile

	surveysFile = pandas.read_excel(newestFile, sheetname=1).to_dict(orient='records')

	return [row for row in surveysFile if row['TL'] == settings['TL']]

def no_eta(rowofdata):
	"""This method accepts a row of data which is
	in the no eta substatus, and then does something
	with it. 
	"""
	scnumber=rowofdata['SC Number']
	dateopened = rowofdata['Date Opened'].to_pydatetime()
	lastUpdated = rowofdata['SR/Activity Last Update '].to_pydatetime()

def getmyfsndata(SRNumber):
	driver = webdriver.Ie()
	driver.maximize_window()
	


if __name__ == '__main__':
	print(getNewestFile())