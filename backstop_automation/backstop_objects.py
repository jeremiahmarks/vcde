# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-05-26 23:27:33
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-05-31 08:00:26


#This file exists in order to provider some basic objects for SRs, SPs, Stores, and backstop reports.


import datetime
import os


sftp_format_string = "Petsmart_Backstop_%m-%d-%Y_at_%H.%M.xlsx"

colsInOrder = ["SR #", "Date Opened", "Days Since Open", "Priority", "SR Substatus", "SR Short Description", "LOS", "Site Area", "City", "State", "Site #", "SC Name", "TL", "SR/Activity Last Update "]



class ServiceRequest(object):
	"""docstring for ServiceRequest"""
	def __init__(self, line_of_data, bs_ts = None):
		super(ServiceRequest, self).__init__()
		self.line_of_data = line_of_data
		self.sr = line_of_data['SR #']
		self.site = line_of_data['Site #']
		self.sp = line_of_data['SC Number']
		self.sp_name = line_of_data['SC Name']
		self.date_opened = line_of_data['Date Opened']
		self.time_open = line_of_data["Days Since Open"]
		self.priority = line_of_data["Priority"]
		self.tl = line_of_data["TL"]
		self.los = line_of_data["LOS"]
		self.short_description = line_of_data["SR Short Description"]
		self.status = line_of_data["SR Substatus"]
		self.nte = line_of_data["NTE"]
		self.ot = line_of_data['Overtime Allowed ']
		self.backstop_timestamp = bs_ts

	def __eq__(self, otherobject):
		if (type(otherobject) == type(" ")):
			return otherobject == self.sr
		else:
			return otherobject.sr == self.sr


class BackStopReport(object):
	"""docstring for BackStopReport"""
	def __init__(self, path):
		super(BackStopReport, self).__init__()
		self.path = path
		self.srs = {}
		self.backstop_timestamp = datetime.datetime.strptime(os.path.basename(self.path), sftp_format_string)

	def load(self):
		self.raw_file = pandas.read_excel(self.path, sheetname=1).to_dict(orient='records')
		for record in self.raw_file:
			self.srs[record['SR #']] = ServiceRequest(record, self.backstop_timestamp)

	def compare(self, previous_backstop, further_backstops=[]):
		mysrs = list(self.srs.keys())
		previous_srs = list(previous_backstop)





		