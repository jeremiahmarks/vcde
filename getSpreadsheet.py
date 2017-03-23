# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-03-21 17:48:30
# @Last Modified by:   jemarks
# @Last Modified time: 2017-03-22 19:52:09

#This script will find the most recent spreadsheet with 
#needed surveys and then download it to the users desktop
#
#Filename template:
	#Jobscomplete_Wo_Survey_Scottsdale_MM.DD.YYYY_at_HH.MM.xlsx
#
#folder path
	#//bos-mart.ip-tech.com/FSNPublishedReports/Operations/



#glob exists to match file names
import glob
import datetime
import pandas


class surveyLineItem():
	"""The surveyLineItem class is designed to parse text into meaningful
	types as well as to hold the information.
	"""
	def __init__(self, lineData):
		self.sr = lineData['SR Num']
		self.dateComplete = datetime.datetime.strptime(lineData ['Complete Date'], '%m/%d/%y').date()
		self.siteNumber = int(lineData ['Site #'])
		self.lineOfService = lineData['LOS']

class PetmLocation():
	"""The PetmLocation class is designed to hold all of the SRs associated 
	with one location and to keep track of the oldest SR at that location.
	"""
	def __init__(self, siteNumber):
		self.siteNum = siteNumber
		self.oldestSR = datetime.date.today()
		self.allSRs = []

	def addSurvey(self, surveyLineItem):
		if surveyLineItem.dateComplete < self.oldestSR:
			self.oldestSR = surveyLineItem.dateComplete
		self.allSRs.append(surveyLineItem)

	def getSearchString(self):
		return " OR ".join([sr.sr for sr in self.allSRs])

class surveyPresenter():
	"""This class will hold which surveys who is doing.
	"""
	def __init__(self, name, maxSurveys=10):
		self.name = name
		self.surveyQueue = []
		self.maxSurveys = 10
		self.sites=[]

	def groupSingles(self):
		"""This method will group all of the sites that
		only have one SR.
		"""
		pass


fileSearchString = "//bos-mart.ip-tech.com/FSNPublishedReports/Operations/Jobscomplete_Wo_Survey_Scottsdale_*"
strpFormatString = "//bos-mart.ip-tech.com/FSNPublishedReports/Operations\\Jobscomplete_Wo_Survey_Scottsdale_%m.%d.%Y_at_%H.%M.xlsx"

columnsToAdd = ["Name", "Completed"]
columnsInOriginalFile = ["SR Num", "Site #", "State", "Time Zone", "LOS", "Days passed since Completed", "Caller Name", "CRM"]

allColumns = columnsToAdd + columnsInOriginalFile


#First Thing - Find the most recent file
matchingFiles = glob.glob(fileSearchString)

newestFile = matchingFiles[0]
for eachfile in matchingFiles:
	if datetime.datetime.strptime(eachfile, strpFormatString) > datetime.datetime.strptime(newestFile, strpFormatString):
		newestFile = eachfile

surveysFile = pandas.read_excel(newestFile).to_dict(orient='records')

