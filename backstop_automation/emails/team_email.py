# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-05-29 19:35:43
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-30 18:32:04


def body(all_stats, all_crits, tl_stats, tl_crits):
	"""Nope, I need to compare the last one, at least. 
	"""
	html_body = "<p>Hello!</p><p>There are " + str(all_stats[0]) + " SRs total. Of those there are " + str(all_crits[0]) + "criticals. "
	html_body += "Of the criticals there are " + str(all_crits[5]) + " Critical SRs in a negative status.</p> "
	html_body += "<p>The oldest SR is from " + str(all_stats[1]) + ". SR #: " + str(all_stats[2]) + "</p>" + "</br></br>"
	html_body += "<p>Your team has " + str(tl_stats[0]) + " SRs  on the backstop. The oldest is from " + str(tl_stats[1]) + " SR: " + str(tl_stats[2])
	html_body += ". The deades SR hasn't moved since " + str(tl_stats[3]) + " SR: " + str(tl_stats[4]) + ".</p></br></br>"
	html_body += "<p> There are " + str(tl_crits[0]) + " criticals on your team, with " + str(tl_crits[5]) + " criticals with a negative status. "
	html_body += "</p><p>" + str(tl_crits[6]) + "</p>"
	return html_body



def body_all(all_stats, all_crits):
	html_body = "<p>Hello!</p> <p>There are"

