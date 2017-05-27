# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 20:37:38
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-05-27 02:33:34

# This file will house all of the various actions to take when there is a new file

import file_man
import petm_teams



negative_statuses=["No ETA", "Quote Required", "Quote Received", "New ETA Required", "No Time Out", "Job Not Complete", "Quoted - Approved by Customer", "Unassigned", "Assigned to Service Contractor"]

def new_file(local_file):
	"""This is the action called when there is a new file.
	It is basically the method used to generate all of the email stuff.
	"""
	# We will need to generate the email to send. Before we can really do that
	# though we will gather the stats we want to drop into the template. 

	# Some data to get:

	# Total SRs on backstop:
	# Total SRs in bad status:
	# Oldest SR Age:
	# Deadest SR (SR with most days since movement):
	# Total Criticals on backstop:
	# Total Criticals in bad status:
	# Total SRs removed from backstop in 24 hours:
	# Total SRs removed from backstop in last hour:
	# Total SRs added to backstop in last 24 hours:
	# Total SRs added to backstop since last report:
	# Total SRs on backstop for TL:
	# Total SRs in bad status for TL:
	# Oldest SR Age for TL:
	# Deadest SR (SR with most days since movement) for TL:
	# Total Criticals on backstop for TL:
	# Total Criticals in bad status for TL:
	# Total SRs removed from backstop in 24 hours for TL:
	# Total SRs removed from backstop in last hour for TL:
	# Total SRs added to backstop in last 24 hours for TL:
	# Total SRs added to backstop since last report for TL:

	# Lets start by getting the other files we will need.
	
	last_backstop = file_man.get_previous_backstop(local_file)

def get_report_stats(report, team_lead=False):
	report_data = pandas.read_excel(report, sheetname=1)
	grouped_by_tl = report_data.groupby('TL')
	overview_scope_all = collect_stats_on_group(report_data)

def collect_stats_on_group(dataframe_of_srs):
	# Okay, look, I want the same basic data on several different subsets
	# of data. There was not a pretty way to do this. 
	total_srs = len(dataframe_of_srs)
	oldest_sr = dataframe_of_srs[dataframe_of_srs['Date Opened'] == dataframe_of_srs['Date Opened'].min()]
	oldest_sr_date = oldest_sr['Date Opened'].values[0]
	oldest_sr_number = oldest_sr['SR #'].values[0]
	deadest_sr = dataframe_of_srs[dataframe_of_srs['SR/Activity Last Update '] == dataframe_of_srs['SR/Activity Last Update '].min()]
	deadest_sr_date = deadest_sr['SR/Activity Last Update '].values[0]
	deadest_sr_number = deadest_sr['SR #'].values[0]
	negative_srs = dataframe_of_srs[dataframe_of_srs['SR Substatus'].isin(negative_statuses)]
	total_negative = len(negative_srs)
	negative_search_string = ' OR '.join([x for x in negative_srs['SR #']])
	return(total_srs, oldest_sr_date, oldest_sr_number, deadest_sr_date, deadest_sr_number, total_negative, negative_search_string)



	
