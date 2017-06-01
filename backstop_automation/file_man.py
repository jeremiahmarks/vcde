# -*- coding: utf-8 -*-
# @Author: jemarks
# @Date:   2017-05-26 18:42:49
# @Last Modified by:   jemarks
# @Last Modified time: 2017-05-31 19:22:37

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

def get_remote_files():
	return sorted(glob.glob(os.path.join(remote_directory, file_search_string)), key = lambda x: datetime.datetime.strptime(x, os.path.join(remote_directory, sftp_format_string)), reverse=True)

def get_local_files():
	return sorted(glob.glob(os.path.join(BS_Folder, file_search_string)), key = lambda x: datetime.datetime.strptime(x, os.path.join(BS_Folder, sftp_format_string)), reverse=True)

def get_all_remote_files():
	remote_files = sorted(glob.glob(os.path.join(remote_directory, file_search_string)), key = lambda x: datetime.datetime.strptime(x, os.path.join(remote_directory, sftp_format_string)), reverse=True)
	needed_files = []
	for eachfile in remote_files:
		file_name = os.path.basename(eachfile)
		local_file_name = os.path.join(BS_Folder, file_name)
		if not(os.path.exists(local_file_name)):
			needed_files.append(eachfile)
	for each_file in needed_files:
		get_specific_file(each_file)

def check_for_new():
	# If there is a new file, this will return the
	# path to the file. If there is not it will 
	# return None
	newest_file = get_remote_files()[0]
	# print(newest_file, "fileman1")
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
	return local_file_path

def get_time_stamp(file_path):
	filename = os.path.basename(file_path)
	timeStamp = datetime.datetime.strptime(filename, sftp_format_string)
	return timeStamp

def get_julian_stamp(file_path):
	filename = os.path.basename(file_path)
	timestamp = datetime.datetime.strftime(datetime.datetime.strptime(filename, sftp_format_string), '%y%j%H%M')
	return int(timestamp)

def get_previous_backstop(local_file_path):
	"""This method will accept the path to an SR and then find the SR immediatly 
	before it."""
	local_files = get_local_files()
	if local_file_path in local_files:
		next_file_location = local_files.index(local_file_path) + 1
		if next_file_location >= len(local_files):
			return None
		return local_files[next_file_location] 
