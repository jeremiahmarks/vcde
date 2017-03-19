#surveyData will exist to accept a URL and then get the data for 
#surveys assigned to me. It will output a single search string
#with all assigned SRs ORd together.

#Eventually this will break the SRs up by the store number and, perhaps add
#controls which control IE to page through the options. 

# temporaryTestingURL="https://docs.google.com/spreadsheets/d/1ELFMvDBhuROF9nMKpvMHQT8jLwOuvDIOUy1_hxYsda8/edit?usp=sharing"
import requests
import csv
from collections import defaultdict 

global CSVSuffix
global fileStoragePath

spreadsheetURL = ""
CSVSuffix = "export?format=csv"
fileStoragePath = "C:////Users//Jeremiah//Desktop//tout.csv"

class surveyLineItem():
	def __init__(self, lineData):
		self.sr = lineData['SR Num']
		self.dateComplete = datetime.datetime.strptime(lineData ['Complete Date'], '%m/%d/%y').date()
		self.siteNumber = int(lineData ['Site #'])
		self.lineOfService = lineData['LOS']

class PetmLocation():
	def __init__(self, siteNumber):
		self.siteNum = siteNumber
		self.oldestSR = datetime.date.today()
		self.allSRs = []

	def addSurvey(self, surveyLineItem):
		if surveyLineItem.dateComplete < self.oldestSR:
			self.oldestSR = surveyLineItem.dateComplete
		self.allSRs.append(surveyLineItem)



def getDocument():
	spreadsheetURL = str(raw_input("Please enter the URL:\n"))
	lastSlash = spreadsheetURL.rfind("/")
	csvDownloadUrl = spreadsheetURL[:lastSlash+1] + CSVSuffix
	surveyData = requests.get(csvDownloadUrl)
	with open(fileStoragePath, 'wb') as outfile:
		outfile.write(a.text)
		#In case you're wondering, "with" closes the file for me
	with open(fileStoragePath, 'rb') as infile:
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
