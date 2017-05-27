# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 18:20:32
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-26 22:03:32

import time
import ctypes

import file_man
import actions_man
import mouse_man

user = ctypes.windll.User32

def is_locked():
	return user.GetForegroundWindow() == 0

def main():
	while True:
		try:
			print("Checking")
			new_file = file_man.check_for_new()
			if new_file:
				print("New File!")
				local_file = file_man.get_specific_file(new_file)
				actions_man.new_file(local_file)
			if is_locked():
				mouse_man.jiggle()
		except Exception as e:
			print(e)
		finally:
			for cycle in range(10):
				print(str(300 - (cycle*30)) + " seconds left")
				time.sleep(30)

if __name__ == '__main__':
	main()

