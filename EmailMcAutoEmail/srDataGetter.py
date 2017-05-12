# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-11 19:23:37
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-11 20:00:18

####################
## Yes, it is python and I am using a Getter.
## Get over it.
##

## This module exists in order to provide the integration
## with the myfsn website. Basically it will scrape the SR
## and parse out valuable information such as the service
## providers email address and notes left on the SR.
from robobrowser import RoboBrowser

class FSNScraper(object):
	"""This module will exists in order to...
	read above. """
	username_field = 'ctl00$ContentPlaceHolder1$tbxUname'
	password_field = 'ctl00$ContentPlaceHolder1$tbxPword'
	def __init__(self):
		super(FSNScraper, self).__init__()
		self.bsr = RoboBrowser()

	def login(self, username, password):
		self.bsr.open('https://myfsn.biz/')
		loginform = self.bsr.get_form()
		loginform[self.username_field].value = username
		loginform[self.password_field].value = password
		self.bsr.submit_form(loginform)

	def get_sr_details(self, srnumber):
		sr_url = 'https://myfsn.biz/SC_Main/SC_SRDetail.aspx?AllowAnyTech=Y&srid=' + srnumber
		self.bsr.open(sr_url)
		print (self.bsr.parsed.getText().replace('\r', '').replace('\n', ''))


