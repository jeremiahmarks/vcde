# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 18:42:49
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-26 19:53:47

# Methods I currently am using elsewhere
# file_man.check_for_new()
# file_man.get_specific_file(new_file)

import glob
import datetime
import os
import shutil


# Provide strings to represent path to file and parsing instructions
file_search_string = "Petsmart_Backstop_*"
remote_directory = "\\\\bos-mart.ip-tech.com\\FSNPublishedReports\\ITDevelopment\\"
sftp_format_string = "Petsmart_Backstop_%m-%d-%Y_at_%H.%M.xlsx"

home_dir = os.path.expanduser('~')
BS_Folder = os.path.join(home_dir, 'BS_report')
if not os.path.exists(BS_Folder):
	os.makedirs(BS_Folder)


def check_for_new():
	# If there is a new file, this will return the
	# path to the file. If there is not it will 
	# return None
	newest_file = sorted(glob.glob(os.path.join(remote_directory, file_search_string)), key = lambda x: datetime.datetime.strptime(x, os.path.join(remote_directory, sftp_format_string)), reverse=True)[0]
	newest_file_name = os.path.basename(newest_file)
	newest_file_local_path = os.path.join(BS_Folder, newest_file_name)
	if not (os.path.exists(newest_file_local_path)):
		return newest_file
	return None

def get_specific_file(file_path):
	# This method will copy the given file from the 
	# given location to the BS_Folder
	local_file_name = os.path.basename(file_path)
	local_file_path = os.path.join(BS_Folder, local_file_name)	
	shutil.copyfile(file_path, local_file_path)