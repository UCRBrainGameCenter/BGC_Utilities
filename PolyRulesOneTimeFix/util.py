import datetime
import json
import keys
import re
import os

def dictionary_keys(dictionary):
	keys = []
	for key in dictionary:
		keys.append(key)

	return keys

def get_user_summary_files(user_files):
	summary_files = []

	for file_name in user_files:
		if keys.SUMMARY in file_name:
			summary_files.append(file_name)

	return summary_files

def get_user_files(directory, user_name):
	all_files = os.listdir(directory)
	files = []

	for file_name in all_files:
		if user_name in file_name:
			files.append(file_name)

	return files

def get_session_files(user_files, session_date):
	session_files = []
	for file_name in user_files:
		if session_date in file_name and keys.SUMMARY not in file_name:
			session_files.append(file_name)

	return session_files

def get_date_from_file_name(file_name):
	return file_name.split('.json')[0][-17:-9]

def get_hours_minutes_seconds_from_file_name(file_name):
	return file_name.split('.json')[0][-8:]

def get_full_time_stamp_from_file_name(file_name):
	return file_name.split('.json')[0][-17:]

def files_with_level(files, level):
	'''
	has to handle the case where levels are presented like '*level_63' but
	also the case where the swap log doesn't have the level before it and 
	is instead '*swap_log63*'
	'''
	level_string = 'level' + str(int(level)) + "_"
	swap_level_string = 'swap_log' + str(int(level)) + "_"
	level_files = []

	for file_name in files:
		if level_string in file_name: # @todo; udpate to use level string
			level_files.append(file_name)
		elif swap_level_string in file_name: # @todo: update to use swap_level_string
			level_files.append(file_name)

	return level_files

def get_generated_shapes_file(level_files):
	files = []
	for file_name in level_files:
		if 'generated_shapes' in file_name:
			files.append(file_name)

	return sorted(files)

def get_user_drag_events(level_files):
	files = []
	for file_name in level_files:
		if 'user_drag_events' in file_name:
			files.append(file_name)

	if len(files) > 0:
		return sorted(files)
	else:
		return None

def get_user_response(level_files):
	files = []
	for file_name in level_files:
		if 'user_response' in file_name:
			files.append(file_name)

	if len(files) > 0:
		return sorted(files)
	else:
		return None

def get_swap_log(level_files):
	files = []
	for file_name in level_files:
		if 'swap_log' in file_name:
			files.append(file_name)

	if len(files) > 0:
		return sorted(files)
	else:
		return None

def remove_from_list(l, val):
	if val != None and val in l:
		l.remove(val)

def find_matching_files(session_files, regular_expression):
	files = []
	regex = re.compile(regular_expression)

	for file_name in session_files:
		if regex.search(file_name):
			files.append(file_name)

	return files

def sort_if_not_null(array):
	if array != None:
		return sorted(array)

	return array

def convert_to_closest_time(files, hours_minutes_seconds):
	if files == None or hours_minutes_seconds == None:
		return None

	max_time_in_seconds = 41
	hours, minutes, seconds = hours_minutes_seconds.split('_')
	original_date = datetime.datetime(2018, 12, 12, int(hours), int(minutes), int(seconds))
	file = None

	for file_name in files:
		hours, minutes, seconds = get_hours_minutes_seconds_from_file_name(file_name).split('_')
		new_date = datetime.datetime(2018, 12, 12, int(hours), int(minutes), int(seconds))

		if abs((new_date - original_date).total_seconds()) < max_time_in_seconds:
			file = file_name
			break

	return file

def file_to_json(directory, file_name):
	if file_name == None:
		return {}
	else:
		json_str = open(os.path.join(directory, file_name), 'r').read()
		return json.loads(json_str)

def get_file_user_name(file_name):
	split = file_name.split('_')
	index = 0
	user_name = ""

	while index < len(split):
		try:
			int(split[index])
			break
		except:
			user_name += split[index] + "_"
			index += 1

	return user_name[:-1]