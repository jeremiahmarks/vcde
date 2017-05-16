# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-12 19:28:29
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-15 19:54:02

# This class exists because our website uses silly ajax for the
# internal notes and robobrowser does not deal with it well.
# I have spent a couple of hours trying to figure out how to 
# check a box. We're taking selenium. 

from selenium import webdriver
import selenium

class SRScraper(object):
	"""This class exists to scrape SR data"""
	def __init__(self):
		super(SRScraper, self).__init__()
		self.driver = webdriver.Ie()
		self.driver.maximize_window()

	def login(self, username, password):
		self.driver.get('https://myfsn.biz')
		element = self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$tbxUname')
		element.send_keys(username)
		element = self.driver.find_element_by_name('ctl00$ContentPlaceHolder1$tbxPword')
		element.send_keys(password)
		element.send_keys(selenium.webdriver.common.keys.Keys.ENTER)
		
	def get_sr_details(self, srnumber):
		sr_url = 'https://myfsn.biz/SC_Main/SC_SRDetail.aspx?AllowAnyTech=Y&srid=' + srnumber
		self.driver.get(sr_url)
		checkbox_id = 'ctl00_ContentPlaceHolder1_systemNotesCheckbox'
		self.driver.find_elements_by_id(checkbox_id).send_keys(webdriver.common.keys.Keys.SPACE)
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
		# Description
		# Special Instruction
		# SP
		# All the notes. 
		# Need all elements of class infoGridRow, infoRow, and infoRowFull