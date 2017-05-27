# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 20:17:24
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-26 21:01:32

# This module exists to simply jiggle the mouse
import ctypes
import time

mouse_event = ctypes.windll.user32.mouse_event
MOUSEEVENTF_MOVE = 0x0001
def jiggle():
	print("hello!")
	mouse_event(MOUSEEVENTF_MOVE, 0, 0, 0, 0)


if __name__ == '__main__':
	while True:
		jiggle()
		time.sleep(3)
