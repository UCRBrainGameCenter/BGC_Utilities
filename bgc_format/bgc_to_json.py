#!/usr/bin/python
# @author: Colan Biemer

import Config
import json
import os

def meta_data_has_correct_fields(meta_data):
	has_required_fields = True

	for field in Config.RequiredFields:
		if field not in meta_data:
			print field, "not found in meta data"
			has_required_fields = False

	return has_required_fields

def remove_redundant_meta_data_keys(meta_data):
	for field in Config.RedundantFields:
		meta_data.pop(field, None)

def convert_data_to_type(data_value):
	if data_value.upper() == "TRUE":
		return True

	if data_value.upper() == "FALSE":
		return False

	try:
		f = float(data_value)
		return f
	except Exception as e:
		pass

	try:
		j = json.loads(data_value)
		return j
	except Exception as e:
		pass

	return data_value

def parse_data_line(line, meta_data):
	data = line.strip('\r').split(meta_data[Config.Delimiter])
	json_result = {}
	column_mapping_key = Config.Default
	column_mapping_found = False

	for i in range(len(data)):
		# create mapping for column mapping if necessary
		if i == 0:
			if data[0] in meta_data[Config.ColumnMapping]:
				column_mapping_key = data[0]
				column_mapping_found = True
				continue

		key = meta_data[Config.ColumnMapping][column_mapping_key][i - 1]

		if key in meta_data[Config.ValueMapping]:
			if data[i] in meta_data[Config.ValueMapping][key]:
				json_result[key] = meta_data[Config.ValueMapping][key][data[i]]
			else:
				print "Value mapping for " + key + " not found."
				json_result[key] = data[i]
		else:
			json_result[key] = data[i]

		json_result[key] = convert_data_to_type(json_result[key])

	return json_result

def convert_file(file_path):
	correct_format = True
	meta_data = {}
	data      = []

	with open(file_path, 'r') as f:
		content = f.readlines()
		first_line = True

		for line in content:
			line = line.strip(Config.NewLine)

			if line == "":
				continue
			
			if first_line:
				try:
					meta_data = json.loads(line)

					if meta_data_has_correct_fields(meta_data) == False:
						correct_format = False
						break
					else:
						first_line = False
				except:
					correct_format = False
					break
			else:
				data.append(parse_data_line(line, meta_data))
			
	remove_redundant_meta_data_keys(meta_data)
	json_log                  = {}
	json_log[Config.MetaData] = meta_data
	json_log[Config.Data]     = data

	return correct_format, json_log

def convert_directory(directory_path, valid_directory_path, invalid_dirrectory_path):
	for file_name in os.listdir(directory_path):
		file_path = os.path.join(directory_path, file_name)

		if not os.path.isfile(file_path):
			continue

		valid, output = convert_file(file_path)

		if valid:
			output_path = os.path.join(valid_directory_path, file_name)
			output_path = output_path.replace('.bgc', '.json')

			f = open(output_path, 'w')
			f.write(json.dumps(output))
			f.close()
		else:
			output_path = os.path.join(invalid_dirrectory_path, file_name)
			invalid_f = open(file_path, 'r')
			out = open(output_path, 'w')

			lines = invalid_f.readlines()
			for line in lines:
				out.write(line)

			invalid_f.close()
			out.close()

# if this is the calling script, allow the user to specify a file to modify
if __name__ == '__main__':
	import sys

	if len(sys.argv) == 2:
		file_name = sys.argv[1]

		if(os.path.isfile(file_name)):
			if file_name.endswith(".bgc"):
				valid, json_file = convert_file(file_name)

				if valid:
					output_file = file_name.replace(".bgc", ".json")

					f = open(output_file, 'w')
					f.write(json.dumps(json_file, default=lambda o: o.__dict__))
					f.close()

					print "Wrote json file to " + output_file
				else:
					print "Error: " + file_name + " was unable to be parsed. Please look through it for errors."
			else:
				print "Error: " + file_name + " could be found but must have the '.bgc' extension."
		else:
			print "Error: " + file_name + " is not a valid file that can be found."
	else:
		print "please provide the file name to convert."
