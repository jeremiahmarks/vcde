# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-30 18:11:49
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-30 18:31:40
import sqlite3

conn = sqlite3.connect('backstop_background.db')
cur = conn.cursor()

def create_table():
	cur.execute("""CREATE TABLE srs (srnum text, sitenum text, scnum text, scname text, dateopened text, priority text, tl text, los text, shortdes text, substatus text, nte text, otallowed text, createdate text, hour integer, minute integer)""")
	cur.commit()

def add_row(srnum, sitenum, scnum, scname, dateopened, priority, tl, los, shortdes, substatus, nte, otallowed, createdate, hour, minute=0):
	command = "INSERT INTO srs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	cur.execute(command, (srnum, sitenum, scnum, scname, dateopened, priority, tl, los, shortdes, substatus, nte, otallowed, createdate, hour, minute))
	cur.commit()