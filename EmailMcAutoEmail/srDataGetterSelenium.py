# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-12 19:28:29
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-17 18:37:57

# This class exists because our website uses silly ajax for the
# internal notes and robobrowser does not deal with it well.
# I have spent a couple of hours trying to figure out how to 
# check a box. We're taking selenium. 

from selenium import webdriver
import selenium
from collections import defaultdict
from bs4 import BeautifulSoup

class SRScraper(object):
	"""This class exists to scrape SR data"""
	def __init__(self):
		super(SRScraper, self).__init__()
		self.driver = webdriver.Ie()
		self.driver.maximize_window()
		self.driver.implicitly_wait(60)
		self.un = 'jemarks_sc'
		self.pw = ''
		

	def login(self, username = None, password  = None):
		if username is None:
			username = self.un
		if password is None:
			password = self.pw
		self.driver.get('https://myfsn.biz')
		try:
			element = self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$tbxUname')
		except Exception:
			print(Exception)
			self.reconnect()
			element = self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$tbxUname')
		element.send_keys(username)
		element = self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$tbxPword')
		element.send_keys(password)
		element.send_keys(selenium.webdriver.common.keys.Keys.ENTER)
		
	def get_sr_details(self, srnumber):
		sr_url = 'https://myfsn.biz/SC_Main/SC_SRDetail.aspx?AllowAnyTech=Y&srid=' + srnumber
		self.driver.get(sr_url)
		checkbox_id = 'ctl00_ContentPlaceHolder1_systemNotesCheckbox'
		self.driver.find_element_by_id(checkbox_id).send_keys(webdriver.common.keys.Keys.SPACE)
		# Some data to specifically get:
		# Site number
		# Site Limit
		# City
		# State
		# Related SR(s)
		# Site Number
		# Status per myfsn
		# Type/Line of service
		# Reason for call
		# Priority
		# Site Area
		# Site Sub Area
		# Date Opened
		# ETAs and SLA data

		# key_value_solids = self.driver.find_elements_by_class_name("infoRow")
		# self.matched_data=defaultdict(list)
		# for eachKVPair in key_value_solids:
		# 	try:
		# 		childs = eachKVPair.find_elements_by_xpath(".//*")
		# 		self.matched_data[childs[0].text].append(childs[1].text)
		# 	except Exception as e:
		# 		print(e)

		self.sr_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		self.info_rows = self.sr_soup.find_all(attrs = {"class":"infoRow"})
		self.matched_data = defaultdict(list)
		for eachrow in self.info_rows:
			if (eachrow.find(attrs = {'class':'fieldLabel'})) and (eachrow.find(attrs = {'class':'fieldValue'})):
				leftside = eachrow.find(attrs = {'class':'fieldLabel'}).text
				rightside = eachrow.find(attrs = {'class':'fieldValue'}).text
				self.matched_data[leftside].append(rightside)


		# Description
		# Special Instruction
		# SP
		# All the notes. 
		# Need all elements of class infoGridRow, infoRow, and infoRowFull

	def reconnect(self):
		self.connectionurl = self.driver.command_executor._url
		self.connectionsession = self.driver.session_id
		self.driver = webdriver.Remote(command_executor = self.connectionurl, desired_capabilities={})
		self.driver.session_id = self.connectionsession

	def connectTo(self, otherInstance):
		connectionurl = otherInstance.driver.command_executor._url
		connectionsession = otherInstance.driver.session_id
		self.driver = webdriver.Remote(command_executor = connectionurl, desired_capabilities={})
		self.driver.session_id = connectionsession
