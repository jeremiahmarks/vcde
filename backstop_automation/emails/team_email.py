# -*- coding: utf-8 -*-
# @Author: Jeremiah
# @Date:   2017-05-29 19:35:43
# @Last Modified by:   jemarks
# @Last Modified time: 2017-06-02 10:07:58


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


def greeting(team_lead, srs_total, srs_new, srs_closed, critical_total, critical_new, critical_closed):
	html_body = "<h1>Hello Team " + team_lead + "!</h1>"
	html_body += "<p>You currently have " + str(srs_total) + " SRs on the backstop. There are " + str(critical_total) + " SRs which are critical. "
	html_body += " You were able to close " + str(srs_closed) + " SRs and " + str(critical_closed) + " critical since the last backstop. "
	html_body += "There are " + str(srs_new) + " new SRs and " + str(critical_new) + " new critical SR(s).</p>"
	return html_body

def get_searh_strings(stats, title=None):
	"""This will accept a namedTuple and then
	return rows of a table with search strings.
	"""
	html_table = "<table>"
	if title:
		html_table += "<tr><td colspan =\"2\">" + str(title) + "</td></tr>"
	for eachpair in [('new', stats.new), ('continued', stats.continued), ('closed', stats.closed)]:
		html_table += "<tr><td>" + eachpair[0] + "</td><td>"
		html_table += ' OR '.join([x.sr for x in eachpair[1]])
		html_table += "</td></tr>"
	html_table += "</table>"
	return html_table

def overviewTable(stats_all, stats_crits, stats_tl, crits_tl):
	html_table = "<table>"
	html_table += get_row("TL", "Total SRs on BS", "SRs carried over", "SRs added", "SRs closed", "Criticals", "Criticals continued", "Criticals added", "Criticals closed")
	for team_lead in stats_tl:
		html_table += get_row(team_lead, len(stats_tl[team_lead].continued) + len(stats_tl[team_lead].new), len(stats_tl[team_lead].continued), len(stats_tl[team_lead].new), len(stats_tl[team_lead].closed), len(crits_tl[team_lead].continued) + len(crits_tl[team_lead].new), len(crits_tl[team_lead].continued), len(crits_tl[team_lead].new), len(crits_tl[team_lead].closed))
	html_table += get_row("Total", len(stats_all.continued) + len(stats_all.new), len(stats_all.continued), len(stats_all.new), len(stats_all.closed), len(stats_crits.continued) + len(stats_crits.new), len(stats_crits.continued), len(stats_crits.new), len(stats_crits.closed))
	html_table += "</table>"
	return html_table

def get_row(team_lead, current_total, carried_total, new_total, closed_total, current_crit, carried_crit, new_crit, closed_crit):
	html_row = "<tr>"
	for each_item in [team_lead, current_total, carried_total, new_total, closed_total, current_crit, carried_crit, new_crit, closed_crit]:
		html_row += get_cell(each_item)
	html_row += "</tr>\n"
	return html_row

def get_cell(table_data):
	return "<td>" + str(table_data) + "</td>\n"


