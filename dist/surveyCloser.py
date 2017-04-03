# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-04-02 17:08:01
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-04-02 17:27:15

#This is more or less a direct rip off of a
#module from a different directory just moved
#here so that everything can run on one computer


#After thinking about the constraints - since
#I am not needing to run through siebel I
#think I could do this with Requests just as
#easily, but I am going to be lazy for now
#since this is already written and tested. 

#This class exists to make old surveys go away.  
#Survey URLs have the pattern 
#http://scportal.firstservicenetworks.com/Survey/Default.aspx?idx=?&SRNumber=SR_NUM&&Chain=PETM-US&&Site=SITE_NUM&&Agent=JEMARKS&&Date=MONTH%2fDAY%2fYEAR
#The survey is in regular HTML thankfully, not ActiveX like the rest of Siebel
import sys
from urllib.parse import urlencode
import datetime
from selenium import webdriver
import selenium
import csv




class SurveyCloser():
	"""This class is responsible for closing surveys. It will accept the path to
	a CSV document with surveys to close and it will close them
	"""


	BASE_URL="http://scportal.firstservicenetworks.com/Survey/Default.aspx?idx=?&"

	def __init__(self):
		self.driver = webdriver.Ie()
		self.driver.maximize_window()
		

	def close_survey(self, row_of_data):
		surveyURL = self.get_url(row_of_data['SR Num'], int(row_of_data['Site #']))
		self.driver.get(surveyURL)
		try:
			submitButton = self.driver.find_element_by_id('btnSubmit')
			submitButton.submit()
		except selenium.common.exceptions.NoSuchElementException as e:
			#This is in case someone submitted the survey between 
			#the time the source report generates and the time
			#that this runs
			pass

	def close_by_csv(self, pathToCSV):
		with open(pathToCSV, 'r') as infile:
			thisReader = csv.DictReader(infile)
			row_number = 0
			for eachrow in thisReader:
				print (row_number)
				row_number += 1
				self.close_survey(eachrow)

	def get_url(self, sr_num, site_num):
		#Note that the SC number can be added back to this
		#method if it is needed for the database
		payload = {"SRNumber": sr_num}
		payload["Site"] = '%04d' % (site_num, )
		payload['Chain'] = "PETM-US"
		payload['Agent'] = "SURVEYCLOSER"
		#Not sure if that is going to work, it may need to be the siebel users
		#name. For instance "JEMARKS" if it were running through my internet explorer.
		payload['Date'] = datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y')

		return self.BASE_URL + urlencode(payload)

if __name__ == '__main__':
	pathToCSV = sys.argv[1]
	thisCloser = SurveyCloser()
	thisCloser.close_by_csv(pathToCSV)