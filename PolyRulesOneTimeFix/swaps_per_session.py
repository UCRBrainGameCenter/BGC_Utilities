# @author: colan biemer

import json
import os

files = os.listdir('users')
users = {}


for file_name in files:
	user_name = file_name.split('.json')[0]

	if 'EF' not in user_name:
		continue

	swaps       = 0
	sessions    = 0
	trial_count = 0

	json_str = open(os.path.join('users', file_name), 'r').read()
	user = json.loads(json_str)

	sessions += len(user)

	for session in user:
		session = user[session]
		for run in session['runs']:
			user_response = session['runs'][run]['user_response']
			if user_response == None or len(user_response) == 0:
				continue

			for response in user_response['data']:
				if response['swapOccured']:
					swaps += 1

				trial_count += 1

	print  user_name + " had " + str(swaps) + " swaps."
	print  user_name + " had " + str(sessions) + " sessions."
	print  user_name + " had " + str(trial_count) + " trials."
	print "---------------------------------------"