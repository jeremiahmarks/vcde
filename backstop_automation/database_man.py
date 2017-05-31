# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-30 18:11:49
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2017-05-30 21:27:18
import sqlite3
import datetime

conn = sqlite3.connect('backstop_background.db')
cur = conn.cursor()

def create_table():
	cur.execute("""CREATE TABLE srs (srnum text, sitenum text, scnum text, scname text, dateopened text, priority text, tl text, los text, shortdes text, substatus text, nte text, otallowed text, createdate integer, hour integer, minute integer)""")
	conn.commit()

def add_row(srnum, sitenum, scnum, scname, dateopened, priority, tl, los, shortdes, substatus, nte, otallowed, createdate, hour=0, minute=0):
	"""This method expects the date to be julian date formatted. 
	"""
	createdate = convert_to_julian(createdate)
	command = "INSERT INTO srs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	cur.execute(command, (srnum, sitenum, scnum, scname, dateopened, priority, tl, los, shortdes, substatus, nte, otallowed, createdate, hour, minute))
	conn.commit()

def convert_to_julian(timestamp):
	"""this method will accept a datetime object
	and return an integer"""
	return int(datetime.datetime.strftime(timestamp, '%y%j'))

def convert_to_datetime(julian_date):
	"""This method will accept either a string
	or an integer representation of the date

	Eventually this will likely need to check that the 
	date makes sense in case I start adding days to it
	somewhere. 
	"""
	return datetime.datetime.strptime(julian_date, '%y%j')