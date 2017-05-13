# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-12 19:28:29
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-12 20:00:06

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
		