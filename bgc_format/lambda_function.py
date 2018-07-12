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

		key = meta_data[Config.ColumnMapping][column_mapping_key][i]

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

def convert_string(string):
	correct_format = True
	meta_data = {}
	data      = []

	content = string.split('\n')
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

def lambda_handler(event, context):
	correct_format, json_data = convert_string(event['body']['bgc'])

	if correct_format:
		return { 
			"body": json.dumps(json_data), 
			"headers": {"Content-Type": "application/json"}, 
			"statusCode": 200 
		}
	else:
		return {
			"body": "BGC data has incorrect format to convert to json.",
			"statusCode": 400
		}