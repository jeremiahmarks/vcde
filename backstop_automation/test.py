# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 20:41:48
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-31 17:11:51

import ctypes
import time
import file_man
import actions_man
from backstop_objects import BackStopReport



def main():
	file_man.get_all_remote_files()
	newest_local = file_man.get_local_files()[0]
	actions_man.new_file(newest_local)

if __name__ == '__main__':
	main()