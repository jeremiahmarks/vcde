# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-08 17:40:30
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-25 11:06:40

import glob
import datetime
import os
import pandas
import urllib
import subprocess
from selenium import webdriver
import selenium
import time
import win32com.client as win32

from auto_settings import settings

# Provide strings to represent path to file and parsing instructions
fileSearchString = "Petsmart_Backstop_*"
remoteDirectory = "\\\\bos-mart.ip-tech.com\\FSNPublishedReports\\ITDevelopment\\"
strpFormatString = "Petsmart_Backstop_%m-%d-%Y_at_%H.%M.xlsx"

remotefileSearchString = remoteDirectory + fileSearchString
remotestrpFormatString = remoteDirectory + strpFormatString


status_column="SR Substatus"
negative_statuses=["No ETA", "Quote Required", "Quote Received", "New ETA Required", "No Time Out", "Job Not Complete", "Quoted - Approved by Customer", "Unassigned", "Assigned to Service Contractor"]

home_dir = os.path.expanduser('~')
BS_Folder = os.path.join(home_dir, 'BS_report')
if not os.path.exists(BS_Folder):
	os.makedirs(BS_Folder)

curFileName = os.path.join(BS_Folder, "OO_current_bs.xlsx")

colsInOrder = ["SR #", "Date Opened", "Days Since Open", "Priority", "SR Substatus", "SR Short Description", "LOS", "Site Area", "City", "State", "Site #", "SC Name", "TL", "SR/Activity Last Update "]


def getNewestFile():
	#This will return a list of dicts, basically like
	#using csv.DictReader to read into a list.
	matchingFiles = glob.glob(remotefileSearchString)

	newestFile = matchingFiles[0]
	for eachfile in matchingFiles:
		if datetime.datetime.strptime(eachfile, remotestrpFormatString) > datetime.datetime.strptime(newestFile, remotestrpFormatString):
			newestFile = eachfile

	bs_file = pandas.read_excel(newestFile, sheetname=1).to_dict(orient='records')

	uneditedfile = pandas.DataFrame([row for row in bs_file if row['TL'] == settings['TL']])
	uneditedfile.to_excel(curFileName, columns=colsInOrder, index=False)
	print(curFileName)

def newer_file_exists():
	#This will return a list of dicts, basically like
	#using csv.DictReader to read into a list.
	matchingFiles = glob.glob(remotefileSearchString)

	newestFile = matchingFiles[0]
	for eachfile in matchingFiles:
		if datetime.datetime.strptime(eachfile, remotestrpFormatString) > datetime.datetime.strptime(newestFile, remotestrpFormatString):
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
	bs_local_file.to_excel(local_bs_file_path, index=False)
	print("Saved to " + str(local_bs_file_path))
	return local_bs_file_path

def email_Travers(local_file):
	localData = pandas.read_excel(local_file).to_dict(orient='records')
	travers_file = pandas.DataFrame([row for row in localData if row['TL'] == "JTRAVERS"])
	criticals = pandas.DataFrame([row for row in localData if (row['TL'] == "JTRAVERS" and row['Priority'] == "Critical" and row[status_column] in negative_statuses)]).sort_values(by="Days Since Open")
	local_dir = os.path.dirname(local_file)
	origFile = os.path.basename(local_file)
	travers_filename = 'JTRAV' + origFile[:origFile.rfind('.')] + origFile[origFile.rfind('.'):]
	travers_fullpath = os.path.join(local_dir, travers_filename)
	travers_file.to_excel(travers_fullpath, columns=colsInOrder, index=False)
	toAddresses = "Jennifer.Travers@vixxo.com; Devon.Mix@vixxo.com; Michael.Lugo@vixxo.com; Jeremiah.Marks@vixxo.com"
	# toAddresses = "Jeremiah.Marks@vixxo.com"
	subject = "Most recent BackStop report"
	HTMLBody = criticals.to_html(index=False, columns=colsInOrder)
	HTMLBody = "<p>There are currently " + str(len(travers_file)) + " SRs for your team in the BackStop Report.</p></br></br> <p>More Details to come.</p></br>" + HTMLBody
	attachments = [travers_fullpath, local_file]
	send_email(toAddresses, subject, HTMLBody, attachments=attachments)


def email_LZ(local_file):
	localData = pandas.read_excel(local_file).to_dict(orient='records')
	lelz_file = pandas.DataFrame([row for row in localData if row['TL'] == "LELZIE"])
	criticals = pandas.DataFrame([row for row in localData if (row['TL'] == "LELZIE" and row['Priority'] == "Critical" and row[status_column] in negative_statuses)]).sort_values(by="Days Since Open")
	local_dir = os.path.dirname(local_file)
	origFile = os.path.basename(local_file)
	lelz_filename = 'LELZ' + origFile[:origFile.rfind('.')] + origFile[origFile.rfind('.'):]
	lelz_fullpath = os.path.join(local_dir, lelz_filename)
	lelz_file.to_excel(lelz_fullpath, columns=colsInOrder, index=False)
	toAddresses = "Laron.Elzie@vixxo.com; Nathan.Wu@vixxo.com; Kyle.Buggs@vixxo.com; Jeremiah.Marks@vixxo.com"
	# toAddresses = "Jeremiah.Marks@vixxo.com"
	subject = "Most recent BackStop report"
	HTMLBody = criticals.to_html(index=False, columns=colsInOrder)
	HTMLBody = "<p>There are currently " + str(len(lelz_file)) + " SRs for your team in the BackStop Report.</p></br></br> <p>More Details to come.</p></br>" + HTMLBody
	attachments = [lelz_fullpath, local_file]
	send_email(toAddresses, subject, HTMLBody, attachments=attachments)


def send_email(toAddresses, Subject, HTMLBody, textBody='', attachments=[]):
	outlook = win32.Dispatch('outlook.application')
	surveysEmail = outlook.CreateItem(0)
	surveysEmail.To = toAddresses
	surveysEmail.Subject = Subject
	surveysEmail.Body = textBody
	surveysEmail.HTMLBody = HTMLBody
	for each_attachment in attachments:
		surveysEmail.Attachments.Add(each_attachment)
	surveysEmail.Send()

def main():
	while True:
		try:
			new_file = newer_file_exists()
			if new_file:
				print("Getting new file!")
				print(time.strftime('%H%M%S'))
				local_file = getSpecificFile(new_file)
				email_Travers(local_file)
				email_LZ(local_file)

			else:
				print("Nothing to get.")
				print(time.strftime('%H%M%S'))
		except Exception:
			print(str(Exception))
		finally:	
			time.sleep(300)

if __name__ == '__main__':
	main()