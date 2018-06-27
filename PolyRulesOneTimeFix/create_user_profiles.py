# @author: Colan Biemer

from create_user_json_profile import create_user_profile
from tqdm import tqdm
import util
import sys
import os

def get_user_names(directory):
	users = {}
	files = os.listdir(directory)
	for file_name in files:
		user = util.get_file_user_name(file_name)

		if user not in users:
			users[user] = True

	return users

def create_user_profiles(input_directory, output_directory):
	users = tqdm(get_user_names(input_directory))
	for user in users:
		users.set_description(user)
		create_user_profile(input_directory, output_directory, user)

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Format must be 'python create_user_profiles.py {INPUT_JSON_DIRECTORY} {OUTPUT_USER_JSON_DIRECTORY}'"
	else:
		if not os.path.isdir(sys.argv[1]):
			print sys.argv[1] + ' is not a directory.'
		elif not os.path.isdir(sys.argv[2]):
			print sys.argv[2] + ' is not a directory.'
		else:
			create_user_profiles(sys.argv[1], sys.argv[2])