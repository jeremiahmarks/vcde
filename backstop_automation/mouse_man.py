# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 20:17:24
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-26 20:29:53

# This module exists to simply jiggle the mouse
import win32api
import time
import math

def jiggle():
	"""This method exists to jiggle the mouse"""

	for i in range(500):
		x = int(500+math.sin(math.pi*i/100)*500)
		y = int(500+math.cos(i)*100)
		win32api.SetCursorPos((x,y))
		time.sleep(.01)

if __name__ == '__main__':
	jiggle()