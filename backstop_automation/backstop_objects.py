# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-05-26 23:27:33
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-05-26 23:46:02
import datetime
#This file exists in order to provider some basic objects for SRs, SPs, Stores, and backstop reports.

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


