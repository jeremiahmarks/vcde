#surveyData will exist to accept a URL and then get the data for 
#surveys assigned to me. It will output a single search string
#with all assigned SRs ORd together.

#Eventually this will break the SRs up by the store number and, perhaps add
#controls which control IE to page through the options. 

# temporaryTestingURL="https://docs.google.com/spreadsheets/d/1ELFMvDBhuROF9nMKpvMHQT8jLwOuvDIOUy1_hxYsda8/edit?usp=sharing"


###########
# Basic idea of logic flow:
	# Download spreadsheet as CSV
	# group surveys by site number
	# find site with oldest surveys
	# if phone rep has more than 10 surveys
	# 	Next phone rep
	# if there is another rep:
	# 	Assign to phone rep
	# 	repeat
	# else
	# 	end
#####

import requests
import csv
import datetime
from collections import defaultdict 

global CSVSuffix
global fileStoragePath

spreadsheetURL = ""
CSVSuffix = "export?format=csv"
fileStoragePath = "C:////Users//Jeremiah//Desktop//tout.csv"

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

class surveyPresenter():
	"""This class will hold which surveys who is doing.
	"""
	def __init__(self, name, maxSurveys=10):
		self.name = name
		self.surveyQueue = []
		self.maxSurveys = 10

def downloadAndGroupBySite(spreadsheetURL):
	lastSlash = spreadsheetURL.rfind("/")
	csvDownloadUrl = spreadsheetURL[:lastSlash+1] + CSVSuffix
	surveyData = requests.get(csvDownloadUrl)
	with open(fileStoragePath, 'w') as outfile:
		outfile.write(surveyData.text)
		#In case you're wondering, "with" closes the file for me
	siteHolder = {}
	with open(fileStoragePath, 'r') as infile:
		csvReader = csv.DictReader(infile)
		for eachline in csvReader:
			thisline = surveyLineItem(dict(eachline))
			if thisline.siteNumber not in siteHolder.keys():
				siteHolder[thisline.siteNumber] = PetmLocation(thisline.siteNumber)
			siteHolder[thisline.siteNumber].addSurvey(thisline)
	return siteHolder

def sortAndAssign(siteHolder, callers):
	sortedHolder = sorted(list(siteHolder.values()), key=lambda site: site.oldestSR)
	for eachCaller in callers:
		while ( len(eachCaller.surveyQueue) < eachCaller.maxSurveys ):
			for eachsurvey in sortedHolder[0].allSRs:
				eachCaller.surveyQueue.append(eachsurvey)
			sortedHolder = sortedHolder[1:]
	return callers




def getDocument():
	spreadsheetURL = str(input("Please enter the URL:\n"))
	lastSlash = spreadsheetURL.rfind("/")
	csvDownloadUrl = spreadsheetURL[:lastSlash+1] + CSVSuffix
	surveyData = requests.get(csvDownloadUrl)
	with open(fileStoragePath, 'w') as outfile:
		outfile.write(surveyData.text)
		#In case you're wondering, "with" closes the file for me
	with open(fileStoragePath, 'r') as infile:
		csvReader = csv.DictReader(infile)
		mysurveys = []
		for eachline in csvReader:
			if eachline['Name'] == 'Jeremiah':
				mysurveys.append(eachline)
	surveysByStore = defaultdict(list)
	for eachline in mysurveys:
		surveysByStore[eachline['Site #']].append(eachline)
	for eachstore in surveysByStore.keys():
		pass
	return surveysByStore



# n1 = "https://docs.google.com/spreadsheets/d/1ELFMvDBhuROF9nMKpvMHQT8jLwOuvDIOUy1_hxYsda8/export?format=csv"
# r=requests.get(n1)
# r
# r.text
