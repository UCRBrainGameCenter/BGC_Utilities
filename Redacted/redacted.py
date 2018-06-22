# @author: Colan Biemer

from PyPDF2 import PdfFileWriter, PdfFileReader
import Tkinter, tkFileDialog, tkMessageBox
import os

def redact(original_file_location, blocker_file_location):
	output   = PdfFileWriter()
	original = PdfFileReader(file(original_file_location, "rb"))
	blocker  = PdfFileReader(file(blocker_file_location, "rb"))

	if original.getNumPages() != blocker.getNumPages():
		print "original has", original.getNumPages(), "pages while the blocker has", blocker.getNumPages(), "which is invalid."
		return

	for page in xrange(original.getNumPages()):
		output_page = original.getPage(page)
		output_page.mergePage(blocker.getPage(page))

		output.addPage(output_page)

	return output

def redact_files_in_directory(input_directory, output_directory, blocking_file):
	for file in os.listdir(input_directory):
		if os.path.isfile(file):
			print file, "is not a file and cannot be converted"
			continue
		elif file.endswith('.pdf') == False:
			print file, 'does not have the ".pdf" file extension and cannot be converted'
			continue

		output = redact(os.path.join(input_directory, file), blocking_file)
		with open(os.path.join(output_directory, file), 'wb') as file:
			output.write(file)

def get_new_directory_path(window_title, window_message):
	tkMessageBox.showinfo(window_title, window_message);
	return tkFileDialog.askdirectory()

def get_new_file_path(window_title, window_message):
	tkMessageBox.showinfo(window_title, window_message)
	return tkFileDialog.askopenfilename()

if __name__ == '__main__':
	input_directory = get_new_directory_path(
		"Input Directory",
		"Select input directory path with files to be redacted.")

	output_directory = get_new_directory_path(
		"Output Directory", 
		"Select output directory path.")

	blocking_file = get_new_file_path(
		"Blocking File",
		"Select pdf to block all pdf files in input directory " + input_directory)

	if blocking_file.endswith('.pdf') == False:
		print "blocking files must be a pdf file where the extension is '.pdf'"
	else:
		redact_files_in_directory(input_directory, output_directory, blocking_file)

