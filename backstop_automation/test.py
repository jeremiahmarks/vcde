# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 20:41:48
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-30 14:39:44

import ctypes
import time
import file_man
import actions_man


def main():
	newFile = file_man.get_local_files()[0]
	actions_man.new_file(newFile)

if __name__ == '__main__':
	main()