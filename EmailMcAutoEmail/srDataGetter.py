# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-11 19:23:37
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-05-11 23:37:52

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
		print (sr_url)
		# TODO: add something regarding the javascript issue. Here is the 
		# Relevant part of the page, and similar issue from stackoverflow that
		# I can use to template my solution is below.
		# '__doPostBack(\'ctl00$ContentPlaceHolder1$systemNotesCheckbox\',\'\')'
		# function __doPostBack(eventTarget, eventArgument) {
		#     if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
		#         theForm.__EVENTTARGET.value = eventTarget;
		#         theForm.__EVENTARGUMENT.value = eventArgument;
		#         theForm.submit();
		#     }
		# }


		# http://stackoverflow.com/questions/27681731/python-requests-robobrowser-aspx-post-javascript
		# b_e_arg = robobrowser.forms.fields.Input('\<input name="__EVENTARGUMENT" value="" \/\>')

		# b_e_target = robobrowser.forms.fields.Input('\<input name="__EVENTTARGET" value="PhoneListsControl$MasterDataControl$masterList$_ctl0$SelectButton" \/\>')

		# In [30]: form_find_b.add_field(b_e_target)
		# In [31]: form_find_b.add_field(b_e_arg)



