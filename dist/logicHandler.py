# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-03-25 14:40:15
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-03-27 21:41:06

#glob exists to match file names
import glob
import datetime
import os
import pandas
import urllib

#Provide strings to represent path to file and parsing instructions
fileSearchString = "//bos-mart.ip-tech.com/FSNPublishedReports/Operations/Jobscomplete_Wo_Survey_Scottsdale_*"
strpFormatString = "//bos-mart.ip-tech.com/FSNPublishedReports/Operations\\Jobscomplete_Wo_Survey_Scottsdale_%m.%d.%Y_at_%H.%M.xlsx"

#This is the string to pass to the command line for the email
outlookPath = '"C:\\Program Files\\Microsoft Office\\Office15\\Outlook.exe"'
outlookCreateFlag = "/c ipm.note"
outlookEmailAddress = "PetSmart-Scottsdale@fusionmethod.com"

#Provide list of needed and existing columns
columnsToAdd = ["Name", "Completed", "Siebel Search String"]
columnsInOriginalFile = ["SR Num", "Site #", "State", "Time Zone", "LOS", "Days passed since Completed", "Caller Name", "CRM"]
allColumns = columnsToAdd + columnsInOriginalFile

#Set up for local storage
home_dir = os.path.expanduser('~')
vixxoUploadDirectory = os.path.join(home_dir, 'surveyMagic')
if not os.path.exists(vixxoUploadDirectory):
	os.makedirs(vixxoUploadDirectory)

#Adding a temporary path for the output file. 
# dpath = "C:\\Users\\Jemarks\\Desktop\\newfile.csv"
surveyOutFilename = "SurveyOutList" + datetime.date.strftime(datetime.date.today(), '%d%B%Y') + ".csv"
pathToSurveyedOut = os.path.join(vixxoUploadDirectory, surveyOutFilename)


#A List of CSRs. This could be changed later
#to a file with one name per line
CSRs = ["John", "Ringo", "Alice", "Bob", "Jen", "Stan", "Fred", "Barney"]


class surveyLineItem():
	"""The surveyLineItem class is designed to parse text into meaningful
	types as well as to hold the information.
	"""
	def __init__(self, lineData):
		self.sr = lineData['SR Num']
		self.siteNumber = int(lineData ['Site #'])
		self.state = lineData['State']
		self.tz = lineData['Time Zone']
		self.los = lineData['LOS']
		try:
			self.daysSinceComplete = int(lineData['Days passed since Completed'])
		except Exception as e:
			self.daysSinceComplete = lineData['Days passed since Completed']
		self.caller = lineData['Caller Name']
		self.crm = lineData['CRM']
		self.name=""
		self.completed=""
		self.searchString=""

	def getCSVRepresentation(self):
		csvReturn = {}
		csvReturn['SR Num'] = str(self.sr)
		csvReturn['Site #'] = str(self.siteNumber)
		csvReturn['State'] = str(self.state)
		csvReturn['Time Zone'] = str(self.tz)
		csvReturn['LOS'] = str(self.los)
		csvReturn['Days passed since Completed'] = str(self.daysSinceComplete)
		csvReturn['Caller Name'] = str(self.caller)
		csvReturn['CRM'] = str(self.crm)
		csvReturn['Name'] = str(self.name)
		csvReturn['Completed'] = ""
		csvReturn['Siebel Search String'] = self.searchString
		return csvReturn


class PetmLocation():
	"""The PetmLocation class is designed to hold all of the SRs associated 
	with one location and to keep track of the oldest SR at that location.
	"""
	def __init__(self, siteNumber):
		self.siteNum = siteNumber
		self.oldestSR = 0
		self.allSRs = []
		self.csrName=''

	def addSurvey(self, surveyLineItem):
		if surveyLineItem.daysSinceComplete > self.oldestSR:
			self.oldestSR = surveyLineItem.daysSinceComplete
		self.allSRs.append(surveyLineItem)

	def getSearchString(self):
		return " OR ".join([sr.sr for sr in self.allSRs])


	def getCSVLines(self):
		storesCSVLines = []
		searchString = self.getSearchString()
		for eachsr in self.allSRs:
			eachsr.searchString = searchString
			eachsr.name=self.csrName
			storesCSVLines.append(eachsr.getCSVRepresentation())
		return storesCSVLines


class vixxoCSR():
	"""This class will hold which surveys who is doing.
	"""
	def __init__(self, name, maxSurveys=10):
		self.name = name
		self.surveyQueue = []
		self.maxSurveys = maxSurveys
		self.sites=[]

	def groupSingles(self):
		"""This method will group all of the sites that
		only have one SR.
		"""
		self.sites.sort(key=lambda site : len(site.allSRs))

	def getCSVLines(self):
		csvLines = []
		for eachSite in self.sites:
			csvLines = csvLines + eachSite.getCSVLines()
		return csvLines


	def assignToSurveys(self):
		for eachSurvey in self.surveyQueue:
			eachSurvey.name = self.name

def getNewestFile():
	#This will return a list of dicts, basically like
	#using csv.DictReader to read into a list.
	matchingFiles = glob.glob(fileSearchString)

	newestFile = matchingFiles[0]
	for eachfile in matchingFiles:
		if datetime.datetime.strptime(eachfile, strpFormatString) > datetime.datetime.strptime(newestFile, strpFormatString):
			newestFile = eachfile

	surveysFile = pandas.read_excel(newestFile).to_dict(orient='records')

	return surveysFile

def trimDataAndGroup(listOfCSVLines):
	"""This will remove unwanted data from the csv,
	group the stores, then sort by sites with the oldest
	SR
	"""
	#First a place to hold our sites while
	#They're being sorted. Later we will 
	#Convert to a list of sites sorted by
	#Oldest SR
	sitesWithSurveys={}
	surveys_to_close=[]
	for eachline in listOfCSVLines:
		thisline = surveyLineItem(eachline)
		if thisline.daysSinceComplete >=7:
			surveys_to_close.append(thisline.getCSVRepresentation())
			continue
		if thisline.siteNumber not in sitesWithSurveys.keys():
			sitesWithSurveys[thisline.siteNumber] = PetmLocation(thisline.siteNumber)
		sitesWithSurveys[thisline.siteNumber].addSurvey(thisline)

	csvFile = pandas.DataFrame(surveys_to_close)
	csvFile.to_csv(pathToSurveyedOut, columns=allColumns, index=False)

	return sorted(list(sitesWithSurveys.values()), key=lambda site: site.oldestSR, reverse=True)

def collectEmailStats(listOfSites):
	"""Note that this needs to be done
	before assigning the surveys since 
	that shrinks the list
	"""
	total_surveys = sum([len(site.allSRs) for site in listOfSites])
	surveys_older_than_one = 0
	for eachSite in listOfSites:
		surveys_older_than_one +=(len([survey for survey in eachSite.allSRs if survey.daysSinceComplete > 1]))
	return total_surveys, surveys_older_than_one

def assignSurveys(listOfSites, vixxoReps):
	"""This method will accept a list of sites with surveys
	and a list of vixxo reps.  It will then assign the surveys to the
	reps based on their maximum number of surveys.
	"""
	for eachRep in vixxoReps:
		while (len(eachRep.surveyQueue) < eachRep.maxSurveys):
			listOfSites[0].csrName = eachRep.name
			for eachSurvey in listOfSites[0].allSRs:
				eachRep.surveyQueue.append(eachSurvey)
			eachRep.sites.append(listOfSites[0])
			listOfSites = listOfSites[1:]
			if len(listOfSites) == 0:
				break
	return listOfSites, vixxoReps

def getAgents():
	"""For now I am going to use the list of
	agents at the top of the screen. I will 
	likely either create and import a simple
	module or a plain text file.
	"""
	# return [vixxoCSR(rep) for rep in CSRs]

	with open("names.txt", 'r') as infile:
		names = [vixxoCSR(line) for line in infile if line[0] is not '#']
	return names
	#Heck yeah, remembered list comprehensions



def combine_to_csv(surveysFile, agents):
	csvFile = []
	csvFile.append(allColumns)
	for eachAgent in agents:
		theselines = eachAgent.getCSVLines()
		for eachline in theselines:
			csvLine = [eachline[column] for column in allColumns]
			csvFile.append(csvLine)
	for eachSite in surveysFile:
		theselines = eachSite.getCSVLines()
		for eachline in theselines:
			csvLine = [eachline[column] for column in allColumns]
			csvFile.append(csvLine)
	return csvFile

def createEmail(total_surveys, total_old_surveys, spreadsheet_link):
	"""This method exists to create the surveys email
	"""
	outlookString = ""
	outlookString += outlookPath + " "
	outlookString += outlookCreateFlag + " "
	outlookString += '/m "' + outlookEmailAddress
	outlookString += "&subject=Todays%20Survey%20Report&body="
	outlookString += urllib.parse.quote(getEmail(total_surveys, total_old_surveys, spreadsheet_link)) + '"'
	os.popen(outlookString)


	# emailString = """  /m "jeremiah@jlmarks.org&subject=This%20Subject&body=%0AHello%2C%0AWe+have+a+total+of+1+surveys%2C+2+are+over+1+day+old.+Everyone+has+surveys+assigned+to+them%2C+they+need+to+be+done+by+2pm+today.%0A%0A3%0A%0APlease+let+me+know+if+you+have+any+questions%2C%0A%0AThank+you%21%0A" """

def getEmail(total_surveys, total_old_surveys, spreadsheet_link):
	return """
Hello,
We have a total of %s surveys, %s are over 1 day old. Everyone has surveys assigned to them, they need to be done by 2pm today.

%s

Please let me know if you have any questions,

Thank you!
""" % (total_surveys, total_old_surveys, spreadsheet_link)
