# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-03-31 15:39:38
# @Last Modified by:   jemarks
# @Last Modified time: 2017-03-31 18:37:49

#This class exists to make old surveys go away.  
#Survey URLs have the pattern 
#http://scportal.firstservicenetworks.com/Survey/Default.aspx?idx=?&SRNumber=SR_NUM&&Chain=PETM-US&&Site=SITE_NUM&&Agent=JEMARKS&&Date=MONTH%2fDAY%2fYEAR
#The survey is in regular HTML thankfully, not ActiveX like the rest of Siebel
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

	def __init__(self, pathToCSV):
		self.csv_path = pathToCSV
		self.driver = webdriver.Ie()
		self.driver.maximize_window()
		with open(pathToCSV, 'r') as infile:
			thisReader = csv.DictReader(infile)
			row_number = 0
			for eachrow in thisReader:
				print (row_number)
				row_number += 1
				self.close_survey(eachrow)

	def close_survey(self, row_of_data):
		surveyURL = self.get_url(row_of_data['SR Num'], int(row_of_data['Site #']))
		self.driver.get(surveyURL)
		try:
			submitButton = self.driver.find_element_by_id('btnSubmit')
			submitButton.submit()
		except selenium.common.exceptions.NoSuchElementException as e:
			pass

	def get_url(self, sr_num, site_num):
		payload = {"SRNumber": sr_num}
		payload["Site"] = '%04d' % (site_num, )
		payload['Chain'] = "PETM-US"
		payload['Agent'] = "JEMARKS"
		payload['Date'] = datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y')

		return self.BASE_URL + urlencode(payload)

