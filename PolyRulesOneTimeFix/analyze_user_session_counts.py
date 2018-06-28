# @author: colan biemer

import json
import os

files = os.listdir('users')
users = {}

user_counts = len(files)
sessions = 0

print 'User Session Counts:'
for file_name in files:
	user_name = file_name.split('.json')[0]

	json_str = open(os.path.join('users', file_name), 'r').read()
	user = json.loads(json_str)

	sessions += len(user)

	print user_name + ": " + str(len(user))

print 
print  'Average Sessions per user: ' +  str(sessions / float(user_counts))