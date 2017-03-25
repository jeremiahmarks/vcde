# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-03-21 17:48:30
# @Last Modified by:   jemarks
# @Last Modified time: 2017-03-24 18:41:23


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

#Since I am too lazy to figure out how to convert 
#the data into a pandas dataframe and then write
#that to a csv, we're just going straight there. 
import csv

#Provide strings to represent path to file and parsing instructions
fileSearchString = "//bos-mart.ip-tech.com/FSNPublishedReports/Operations/Jobscomplete_Wo_Survey_Scottsdale_*"
strpFormatString = "//bos-mart.ip-tech.com/FSNPublishedReports/Operations\\Jobscomplete_Wo_Survey_Scottsdale_%m.%d.%Y_at_%H.%M.xlsx"

#Provide list of needed and existing columns
columnsToAdd = ["Name", "Completed", "Siebel Search String"]
columnsInOriginalFile = ["SR Num", "Site #", "State", "Time Zone", "LOS", "Days passed since Completed", "Caller Name", "CRM"]
allColumns = columnsToAdd + columnsInOriginalFile

#Adding a temporary path for the output file. 
dpath = "C:\\Users\\Jemarks\\Desktop\\newfile.csv"

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




#First Thing - Find the most recent file
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

	for eachline in listOfCSVLines:
		thisline = surveyLineItem(eachline)
		if thisline.daysSinceComplete >=7:
			continue
		if thisline.siteNumber not in sitesWithSurveys.keys():
			sitesWithSurveys[thisline.siteNumber] = PetmLocation(thisline.siteNumber)
		sitesWithSurveys[thisline.siteNumber].addSurvey(thisline)

	return sorted(list(sitesWithSurveys.values()), key=lambda site: site.oldestSR, reverse=True)

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
	return [vixxoCSR(rep) for rep in CSRs]
	#Heck yeah, remembered list comprehensions

def main():
	"""This is the script that puts everything
	together.
	"""
	agents=getAgents()
	surveysFile = getNewestFile()
	sortedSites = trimDataAndGroup(surveysFile)
	sortedSites, agents = assignSurveys(sortedSites, agents)
	csvFile = []
	for eachAgent in agents:
		csvFile = csvFile + eachAgent.getCSVLines()
	for eachSite in sortedSites:
		csvFile = csvFile + eachSite.getCSVLines()
	csvFile = pandas.DataFrame(csvFile)
	csvFile.to_csv(dpath, columns=allColumns, index=False)
	# return csvFile
	# with open(pathToDesktop) as outfile:




#Todo:
	# Create vixxoReps
	# Assign reps to each line
	# output to csv
	# Change trimDataAndGroup to not include SRs over the max age
	# Update the surveyLineItem who's assigned to it
	# Give the vixxoCSR a way to sort their SRs into groups of single/multiple survey per site


#Far in the future to do:
	# use requests to log in to the google docs account
	# count the stats
	# generate the body of the email for copy paste ease

