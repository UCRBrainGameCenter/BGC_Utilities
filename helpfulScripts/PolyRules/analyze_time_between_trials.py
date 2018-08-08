# @author: colan Biemer

import platform
import json
import sys
import os
import re

USER_RESPONSE = "user_response"
SWAP_LOG      = "swap_log"
EXTENSION     = ".json"

def is_directory_of_only_json_files(path):
	valid = True
	if os.path.isdir(path) == False:
		print "'" + path + "' is not a directory."
		valid = False
	else:
		for file_name in os.listdir(path):
			if file_name.endswith('.json') == False:
				print "'" + path + "' can only contain json files, yet '" + file_name + "' was found."
				valid = False
				break

	return valid

def analyze_time_between_trials(path):
	total_trial_inbetween_time = 0
	trial_count = 0

	for file_name in os.listdir(path):
		if SWAP_LOG not in file_name:
			continue

		# get user response log file name and modify it so the last part of the time stamp
		# is a wild card since it may be off by 1
		user_response_file = file_name.replace(SWAP_LOG, USER_RESPONSE)
		user_response_file = user_response_file[:user_response_file.index(USER_RESPONSE) + len(USER_RESPONSE) + 17] \
		                   + ".*" + user_response_file[user_response_file.index(EXTENSION):]

		regex = re.compile(user_response_file)
		found = False
		for f in os.listdir(path):
			if regex.match(f):
				user_response_file = f
				found = True
				break

		if found == False:
			print file_name + " had no easy to match user response log."
			continue

		user_response = json.load(open(path + user_response_file, 'r'))
		swap_info = json.load(open(path + file_name, 'r'))
		swap_trials = []

		for j in range(len(swap_info['data'])):
			swap_trials.append(int(swap_info['data'][j]['trial']))

		length = len(user_response['data'])
		for j in range(length):
			# skip swap trials, else go forward with calculations
			if j + 1 in swap_trials:
				continue

			if j + 1 < length:
				trial_count += 1
				total_trial_inbetween_time += user_response['data'][j+1]['startTime'] - user_response['data'][j]['endTime']

	print "Average ITI (ms): ", total_trial_inbetween_time / float(trial_count)

if __name__ == '__main__':
	if platform.system() == "Windows":
		print "This program is unable to run on windows"
	elif len(sys.argv) != 2:
		print "Must supply argument that points to the directory of logs"
	else:
		path = sys.argv[1]

		if path.endswith("/") == False:
			path += "/"

		if is_directory_of_only_json_files(path):
			analyze_time_between_trials(path)
