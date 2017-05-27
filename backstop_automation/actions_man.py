# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 20:37:38
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-26 21:59:04

# This file will house all of the various actions to take when there is a new file

import file_man


teams = {}
teams['JTRAVERS'] = []
teams['JTRAVERS'].append('Jennifer.Travers@vixxo.com')
teams['JTRAVERS'].append('Devon.Mix@vixxo.com')
teams['JTRAVERS'].append('Michael.Lugo@vixxo.com')
teams['JTRAVERS'].append('Jeremiah.Marks@vixxo.com')

teams['LELZIE'] = []
teams['LELZIE'].append('Laron.Elzie@vixxo.com')
teams['LELZIE'].append('Kyle.Buggs@vixxo.com')
teams['LELZIE'].append('Robert.Cottrell@vixxo.com')
teams['LELZIE'].append('Nathan.Wu@vixxo.com')


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
	
