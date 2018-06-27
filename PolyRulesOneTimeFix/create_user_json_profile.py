# @author: Colan Biemer

import util
import json
import keys
import os
import re

def build_unique_sessions(summary_files):
	unique_sessions = {}

	for summary_name in summary_files:
		session = util.get_date_from_file_name(summary_name)
		if session not in unique_sessions:
			unique_sessions[session] = []

		unique_sessions[session].append(summary_name)

	return unique_sessions

def construct_summary_file(directory, session_date, summary_files):
	# sorting the list alphabetically guarantees chronological
	# order due to the file name structure
	summary_files = sorted(summary_files)
	summary_file = None
	run_number = 0

	for file_name in summary_files:
		json_str = open(os.path.join(directory, file_name), 'r').read()
		json_data = json.loads(json_str)

		if summary_file == None:
			summary_file = json_data
		else:
			for line in json_data[keys.DATA]:
				line[keys.RUN_NUMBER] = run_number
				summary_file[keys.DATA].append(line)
				run_number += 1

	return summary_file

def build_session(directory, user_files, session_date, summary_files):
	session = {}
	summary_file = construct_summary_file(directory, session_date, summary_files)
	session_files = util.get_session_files(user_files, session_date)
	runs = {}
	previous_run_number = -1
	run_number_incrementer = 0

	for data in summary_file[keys.DATA]:
		# get files that can retrieved with the level 
		level_files = util.files_with_level(session_files, data[keys.LEVEL])
		generated_shapes = util.get_generated_shapes_file(level_files)
		user_drag_events = util.get_user_drag_events(level_files)
		user_response    = util.get_user_response(level_files)
		swap_log         = util.get_swap_log(level_files)

		# check previous run number to look for crashes
		run_number = int(data[keys.RUN_NUMBER])
		if previous_run_number == run_number:
			if generated_shapes == None or len(generated_shapes) == 0:
				print 'run number ' + str(run_number) + ' is a duplicate with no valid files attached to it.'
				continue
			if rule_log == None or len(rule_log) == 0:
				print 'no existing rule log for run number ' + str(run_number)
				continue
			else:
				run_number_incrementer += 1
		elif generated_shapes == None or len(generated_shapes) == 0:
			print 'no existing generated_shapes for run number ' + str(run_number)
			continue
		else:
			previous_run_number = run_number

		while run_number + run_number_incrementer in runs:
			run_number_incrementer += 1

		run_number += run_number_incrementer

		generated_shapes = util.sort_if_not_null(generated_shapes)[0]
		user_drag_events = util.sort_if_not_null(user_drag_events)
		user_response    = util.sort_if_not_null(user_response)
		swap_log         = util.sort_if_not_null(swap_log)

		# use the generated shape log which is guaranteed to have atleast one 
		# value to find the closest time stamp for the rule log and layout log.
		time_stamp = util.get_date_from_file_name(generated_shapes)
		layout_log = util.find_matching_files(session_files, 'layout_log_' + time_stamp)
		rule_log   = util.find_matching_files(session_files, 'rule_log_' + time_stamp)

		if rule_log == None or len(rule_log) == 0:
			print 'no existing rule log for run number ' + str(run_number)
			continue

		layout_log = util.sort_if_not_null(layout_log)[0]
		rule_log = util.sort_if_not_null(rule_log)[0]

		# user_drag_events, user_response_and swap_log are not guaranteed to exist
		# in the current logging format. So we have to do extra work here to make 
		# sure our time stamps match up else, we leave them for future iterations.
		hours_minutes_seconds = util.get_hours_minutes_seconds_from_file_name(generated_shapes)
		user_drag_events = util.convert_to_closest_time(user_drag_events, hours_minutes_seconds)
		user_response    = util.convert_to_closest_time(user_response, hours_minutes_seconds)
		swap_log         = util.convert_to_closest_time(swap_log, hours_minutes_seconds)

		run_data = {}
		run_data['user_drag_events'] = util.file_to_json(directory, user_drag_events)
		run_data['generated_shapes'] = util.file_to_json(directory, generated_shapes)
		run_data['user_response']    = util.file_to_json(directory, user_response)
		run_data['layout_log']       = util.file_to_json(directory, layout_log)
		run_data['swap_log']         = util.file_to_json(directory, swap_log)
		run_data['rule_log']         = util.file_to_json(directory, rule_log)
		runs[run_number] = run_data

		# remove files from lists since they will no longer be used
		util.remove_from_list(session_files, generated_shapes)
		util.remove_from_list(session_files, user_drag_events)
		util.remove_from_list(session_files, user_response)
		util.remove_from_list(session_files, layout_log)
		util.remove_from_list(session_files, swap_log)
		util.remove_from_list(session_files, rule_log)

		util.remove_from_list(user_files, generated_shapes)
		util.remove_from_list(user_files, user_drag_events)
		util.remove_from_list(user_files, user_response)
		util.remove_from_list(user_files, layout_log)
		util.remove_from_list(user_files, swap_log)
		util.remove_from_list(user_files, rule_log)

	session[keys.SUMMARY] = summary_file
	session[keys.RUNS] = runs
	return session


def create_user_profile(input_directory, output_directory, user_name):
	user_files    = util.get_user_files(input_directory, user_name)
	summary_files = util.get_user_summary_files(user_files)

	sessions = build_unique_sessions(summary_files)
	session_keys = sorted(util.dictionary_keys(sessions))
	session_data = {}

	for i in range(len(session_keys)):
		session_data[str(i)] = build_session(input_directory, user_files, session_keys[i], sessions[session_keys[i]])

	f = open(os.path.join(output_directory, user_name) + '.json', 'w')
	f.write(json.dumps(session_data))
	f.close()

if __name__ == '__main__':
	create_user_profile('one_user_hard_json', 'users', 'EF_T102')