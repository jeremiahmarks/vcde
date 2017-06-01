# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 20:41:48
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-31 20:11:32

# Current objective : generate an image with the history of SRs
import file_man
from backstop_objects import BackStopReport

def main():
	local_files = file_man.get_local_files()
	bs_reports = []
	compared = {}
	for each_file in local_files[:50]:
		jdate = file_man.get_julian_stamp(each_file)
		bs_reports.append(BackStopReport(each_file))
	for each_file in range(len(bs_reports[:-1])):
		compared[bs_reports[each_file].jdate] = bs_reports[each_file].compare(bs_reports[each_file + 1])
	print(compared)






if __name__ == '__main__':
	main()