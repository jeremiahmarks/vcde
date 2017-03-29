# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-03-25 15:23:07
# @Last Modified by:   jemarks
# @Last Modified time: 2017-03-28 19:52:26

import googleAuth
import logicHandler
import sendOutlookEmail

import datetime
import os

def main():
	newDocTitle = "Survey Assignments " + datetime.date.strftime(datetime.date.today(), '%d%B%Y')
	newEmailSubject = datetime.date.strftime(datetime.date.today(), '%d %B %Y') + " Survey Assignments"

	print("Get Agents")
	agents = logicHandler.getAgents()
	print("Get newest files")
	surveysFile = logicHandler.getNewestFile()
	print("Trim and group")
	surveysFile = logicHandler.trimDataAndGroup(surveysFile)

	print("Collect Stats")
	totalSRs, totalOldSRs = logicHandler.collectEmailStats(surveysFile)

	print("Assign Surveys")
	surveysFile, agents = logicHandler.assignSurveys(surveysFile, agents)
	csvFile = logicHandler.combine_to_csv(surveysFile, agents)

	print("upload to google")
	sheetService = googleAuth.getSheetService()
	print("create spreadsheet")
	newSpreadsheet = googleAuth.addSpreadsheet(sheetService, title=newDocTitle)
	print("update spreadsheet values")
	result_of_adding = googleAuth.add_lines_to_spreadsheet(sheetService, newSpreadsheet['spreadsheetId'], csvFile)
	print("change spreadsheet privacy")
	result_of_sharing = googleAuth.shareDocument(newSpreadsheet['spreadsheetId']).execute()
	sheetURL = newSpreadsheet['spreadsheetUrl']

	# emailBody = logicHandler.getEmail(totalSRs, totalOldSRs, sheetURL)
	print("Create Email")
	# logicHandler.createEmail(totalSRs, totalOldSRs, sheetURL)
	emailBody = logicHandler.getEmail(totalSRs, totalOldSRs, sheetURL)
	# emailToAddress = "Jeremiah.Marks@vixxo.com"
	emailToAddress = "PetSmart-Scottsdale@fusionmethod.com"
	emailSubject = newEmailSubject
	sendOutlookEmail.sendEmail(emailToAddress, emailSubject, emailBody)


if __name__ == '__main__':
	main()