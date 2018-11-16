#!/usr/bin/python
# @author: Colan Biemer

import Tkinter, tkFileDialog, tkMessageBox
import bgc_to_json
import sys
import os

def confirm_directory(directory_path):
	return tkMessageBox.askyesno(
		"Directory Confirmation", 
		"Is \"" + directory_path + "\" the correct directory?")

def get_new_directory_path():
	tkMessageBox.showinfo(
		"Output Directory", 
		"Use the next dialogue box to set the output directory");
	return tkFileDialog.askdirectory()

def get_incorrect_directory_path():
	tkMessageBox.showinfo(
		"Incorrect Output Directory", 
		"Use the next dialogue box to set the output directory for files with the incorrect format");
	return tkFileDialog.askdirectory()

def main():
	root = Tkinter.Tk()
	root.withdraw()

	directory_path = tkFileDialog.askdirectory()

	if directory_path == () or directory_path == None:
		print "Operation cancelled. Please select directory for operation to run."
	else:
		if(confirm_directory(directory_path)):
			output_directory = get_new_directory_path()
			error_directory = get_incorrect_directory_path()

			if len(sys.argv) == 2 and sys.argv[1] == "--ipad":
				for user_directory in os.listdir(directory_path):
					user_directory_path = os.path.join(directory_path, user_directory)
					if not os.path.isdir(user_directory_path):
						print "ignoring file", user_directory_path
						continue

					bgc_to_json.convert_directory(
						user_directory_path, 
						output_directory, 
						error_directory)
			else:
				bgc_to_json.convert_directory(directory_path, output_directory, error_directory)

if __name__ == '__main__':
	main()
