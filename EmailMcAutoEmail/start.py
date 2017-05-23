# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-08 17:40:30
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-22 19:20:58

import glob
import datetime
import os
import pandas
import urllib
import subprocess
from selenium import webdriver
import selenium
import time

from auto_settings import settings

# Provide strings to represent path to file and parsing instructions
fileSearchString = "\\\\bos-mart.ip-tech.com\\FSNPublishedReports\\ITDevelopment\\Petsmart_Backstop_*"
strpFormatString = "\\\\bos-mart.ip-tech.com\\FSNPublishedReports\\ITDevelopment\\Petsmart_Backstop_%m-%d-%Y_at_%H.%M.xlsx"




home_dir = os.path.expanduser('~')
BS_Folder = os.path.join(home_dir, 'BS_report')
if not os.path.exists(BS_Folder):
	os.makedirs(BS_Folder)

curFileName = os.path.join(BS_Folder, "OO_current_bs.xlsx")

colsInOrder = ["SR #", "Date Opened", "Days Since Open", "Priority", "SR Substatus", "SR Short Description", "LOS", "Site Area", "City", "State", "Site #", "SC Name", "TL", "SR/Activity Last Update "]


def getNewestFile():
	#This will return a list of dicts, basically like
	#using csv.DictReader to read into a list.
	matchingFiles = glob.glob(fileSearchString)

	newestFile = matchingFiles[0]
	for eachfile in matchingFiles:
		if datetime.datetime.strptime(eachfile, strpFormatString) > datetime.datetime.strptime(newestFile, strpFormatString):
			newestFile = eachfile

	bs_file = pandas.read_excel(newestFile, sheetname=1).to_dict(orient='records')

	uneditedfile = pandas.DataFrame([row for row in bs_file if row['TL'] == settings['TL']])
	uneditedfile.to_excel(curFileName, columns=colsInOrder, index=False)
	print(curFileName)

def newer_file_exists():
	#This will return a list of dicts, basically like
	#using csv.DictReader to read into a list.
	matchingFiles = glob.glob(fileSearchString)

	newestFile = matchingFiles[0]
	for eachfile in matchingFiles:
		if datetime.datetime.strptime(eachfile, strpFormatString) > datetime.datetime.strptime(newestFile, strpFormatString):
			newestFile = eachfile
	newestFileName = os.path.basename(newestFile)
	newestFileFullPath = os.path.join(BS_Folder, newestFileName)
	if not (os.path.exists(newestFileFullPath)):
		return newestFile
	return None


def getSpecificFile(filename):
	"""This method exists to get a specific file. This will be handy when
	checking for when the file is updated. 
	"""

	bs_file = pandas.read_excel(filename, sheetname=1).to_dict(orient='records')
	bs_local_file = pandas.DataFrame([x for x in bs_file]) #This is added because I was sorting things at this stage.
	bs_filename = os.path.basename(filename)
	local_bs_file_path = os.path.join(BS_Folder, bs_filename)
	bs_local_file.to_excel(local_bs_file_path, columns=colsInOrder, index=False)
	print("Saved to " + str(local_bs_file_path))
	return local_bs_file_path

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
	

def main():
	while True:
		new_file = newer_file_exists()
		if new_file:
			print("Getting new file!")
			getSpecificFile(new_file)
		else:
			print("Nothing to get.")
		time.sleep(300)

if __name__ == '__main__':
	main()