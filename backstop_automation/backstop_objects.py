# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-05-26 23:27:33
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-31 20:13:15


#This file exists in order to provider some basic objects for SRs, SPs, Stores, and backstop reports.


import datetime
import os
import pandas
import collections
from petm_teams import teams
from emails import team_email
import file_man

sftp_format_string = "Petsmart_Backstop_%m-%d-%Y_at_%H.%M.xlsx"

colsInOrder = ["SR #", "Date Opened", "Days Since Open", "Priority", "SR Substatus", "SR Short Description", "LOS", "Site Area", "City", "State", "Site #", "SC Name", "TL", "SR/Activity Last Update "]
Stats = collections.namedtuple('Stats', ['new', 'continued', 'closed'])


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
		self.jdate = file_man.get_julian_stamp(self.path)
		self.load()

	def load(self):
		self.raw_file = pandas.read_excel(self.path, sheetname=1).to_dict(orient='records')
		for record in self.raw_file:
			self.srs[record['SR #']] = ServiceRequest(record, self.backstop_timestamp)



	def compare(self, previous_backstop, further_backstops=[]):
		mysrs = list(self.srs.keys())
		previous_srs = list(previous_backstop.srs.keys())
		stats_all = self.compare_subset(mysrs, previous_srs)
		mycrits = [x.sr for x in self.srs.values() if x.priority == "Critical"]
		previous_crits = [x.sr for x in previous_backstop.srs.values() if x.priority == "Critical"]
		stats_crits = self.compare_subset(mycrits, previous_crits)
		stats_tl = collections.defaultdict(list)
		crits_tl = collections.defaultdict(list)
		for teamlead in teams:
			this_tl = [x.sr for x in self.srs.values() if x.tl == teamlead]
			previous_tl = [x.sr for x in previous_backstop.srs.values() if x.tl == teamlead]
			this_tl_crits = [x.sr for x in self.srs.values() if x.tl == teamlead and x.priority == "Critical"]
			previous_tl_crits = [x.sr for x in previous_backstop.srs.values() if x.tl == teamlead and x.priority == "Critical"]
			stats_tl[teamlead] = self.compare_subset(this_tl, previous_tl)
			crits_tl[teamlead] = self.compare_subset(this_tl_crits, previous_tl_crits)
		# print(team_email.overviewTable(stats_all, stats_crits, stats_tl, crits_tl))
		return stats_all, stats_crits, stats_tl, crits_tl

	def compare_subset(self, subset1, subset2):
		# subset1 = list(subset1.keys())
		# subset2 = list(subset2.keys())
		srs_continued=[]
		srs_closed=[]
		srs_new=[]
		for each_sr in subset1:
			if each_sr in subset2:
				srs_continued.append(each_sr)
			else:
				srs_new.append(each_sr)
		for each_sr in subset2:
			if each_sr not in subset1:
				srs_closed.append(each_sr)

		return Stats(new=srs_new, continued=srs_continued, closed=srs_closed)

