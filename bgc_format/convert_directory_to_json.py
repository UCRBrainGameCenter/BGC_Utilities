#!/usr/bin/python
# @author: Colan Biemer

import tkinter as Tkinter, tkinter.filedialog as tkFileDialog, tkinter.messagebox as tkMessageBox
import bgc_to_json
import sys
import os

import argparse

def confirm_directory(directory_path):
	return tkMessageBox.askyesno(
		"Directory Confirmation", 
		"Is \"" + directory_path + "\" the correct directory?")

def get_new_directory_path():
	tkMessageBox.showinfo(
		"Output Directory", 
		"Use the next dialogue box to set the output directory")
	return tkFileDialog.askdirectory()

def get_incorrect_directory_path():
	tkMessageBox.showinfo(
		"Incorrect Output Directory", 
		"Use the next dialogue box to set the output directory for files with the incorrect format")
	return tkFileDialog.askdirectory()

def build_argparser():
	parser = argparse.ArgumentParser(description="BGC to JSON Format Converter for Directories")

	parser.add_argument('--bgc-dir', type=str, help='directory location of for bgc files')
	parser.add_argument('--output-dir', type=str, help='directory location for output json files')
	parser.add_argument('--error-dir', type=str, help='directory for files that could not be converted to json')

	parser.add_argument('--run-gui', action='store_true', help='flag to run a GUI version for non-technical users')

	return parser.parse_args()

if __name__ == '__main__':
	args = build_argparser()
	if args.bgc_dir and args.output_dir and args.error_dir:
		if not os.path.isdir(args.bgc_dir):
			print(f'{args.bgc_dir} is not a valid directory')
		elif not os.path.isdir(args.output_dir):
			print(f'{args.output_dir} is not a valid directory')
		elif not os.path.isdir(args.error_dir):
			print(f'{args.error_dir} is not a valid directory')
		else:
			print('\n')
			print(f'BGC data found in "{args.bgc_dir}"')
			print(f'Successful conversions being sent to "{args.output_dir}"')
			print(f'Unsucceful conversions being sent to: "{args.error_dir}"')
			print('\n')
			bgc_to_json.convert_directory(args.bgc_dir, args.output_dir, args.error_dir)
	elif args.run_gui:
		root = Tkinter.Tk()
		root.withdraw()

		directory_path = tkFileDialog.askdirectory()

		if directory_path == () or directory_path == None or directory_path == "":
			print("Operation cancelled. Please select directory for operation to run.")
		else:
			if(confirm_directory(directory_path)):
				output_directory = get_new_directory_path()
				error_directory = get_incorrect_directory_path()

				if len(sys.argv) == 2 and sys.argv[1] == "--ipad":
					for user_directory in os.listdir(directory_path):
						user_directory_path = os.path.join(directory_path, user_directory)
						if not os.path.isdir(user_directory_path):
							print("ignoring file: " + user_directory_path)
							continue

						bgc_to_json.convert_directory(
							user_directory_path, 
							output_directory, 
							error_directory)
				else:
					bgc_to_json.convert_directory(directory_path, output_directory, error_directory)
	else:
		print('run this with "-h" for help.')