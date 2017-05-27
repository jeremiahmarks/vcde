# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 18:20:32
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-26 18:41:21

import time

def main():
	while True:
		try:
			new_file = file_man.check_for_new()
			if new_file:
				local_file = file_man.get_specific_file(new_file)
				actions_man.newFile(local_file)
			mouse_man.jiggle()
		except Exception as e:
			print(e)
	finally:
		time.sleep(300)

if __name__ == '__main__':
	main()

