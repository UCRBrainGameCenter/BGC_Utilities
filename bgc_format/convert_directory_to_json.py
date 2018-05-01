#!/usr/bin/python
# @author: COlan Biemer

import Tkinter, tkFileDialog, tkMessageBox
import bgc_to_json

def confirm_directory(directory_path):
	return tkMessageBox.askyesno("Directory Confirmation", "Is \"" + directory_path + "\" the correct directory?")

def get_new_directory_path():
	tkMessageBox.showinfo("Output Directory", "Use the next dialogue box to set the output directory");
	return tkFileDialog.askdirectory()

def get_incorrect_directory_path():
	tkMessageBox.showinfo("Incorrect Output Directory", "Use the next dialogue box to set the output directory for files with the incorrect format");
	return tkFileDialog.askdirectory()

def main():
	root = Tkinter.Tk()
	root.withdraw()

	directory_path = tkFileDialog.askdirectory()

	if directory_path == () or directory_path == None:
		print "Operation cancelled. Please select directory for operation to run."
	else:
		if(confirm_directory(directory_path)):
			bgc_to_json.convert_directory(directory_path, get_new_directory_path(), get_incorrect_directory_path())

if __name__ == '__main__':
	main()