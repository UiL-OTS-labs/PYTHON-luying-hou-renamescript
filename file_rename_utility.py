#!/usr/bin/python
import csv, os, shutil

def generate_dictionary_from_csv_file(filepath, lines_to_skip = 2):
	with open(filepath, 'r') as csvfile:
		result = []
		dictionary_reader = csv.DictReader(csvfile, delimiter=';', fieldnames = ['block','trialnum','id','imagefn'])
		row_number = 0
		for row in dictionary_reader:
			row_number +=1
			if(row_number > lines_to_skip):
				parsed_row = parse_integers(row)
				if not line_already_added(parsed_row, result):
					result.append(parsed_row)
		return result

def line_already_added(parsed_row, result):
	for entry in result:
		if entry['id'] == parsed_row['id'] and entry['trialnum'] == parsed_row['trialnum']:
			return True
	return False

def parse_integers(dict):
	for key in dict:
		try:
			dict[key] = int(dict[key])
		except ValueError:
			dict[key] = float('nan')
	return dict

def new_name_for_file(participant_id, dictonary):
	return "%02d_block_%02d_%02d" % (participant_id, dictonary['block'], dictonary['id'])

def get_participant_id_from_folder(foldername):
	result = ""
	for char in foldername:
		if char.isdigit():
			result += char
		else:
			break
	return result

def match_csv_dictionaries_to_files(csv_dictonaries, current_data_folder):
	for file_name in os.listdir(current_data_folder):
		for csv_entry in csv_dictonaries:
			block_id = "block%d" % csv_entry['block']
			trial_id = "test_trial_%02d" % csv_entry['trialnum']
			if block_id  in file_name or (csv_entry['block'] == 0 and "practice" in file_name): 
				if trial_id in file_name:
					associate_file_with_csv(current_data_folder +'/' + file_name, csv_entry)

def associate_file_with_csv(file_name,csv_entry):
	attempt_number = attempt(file_name)
	if not ( csv_entry.has_key('file') and csv_entry.has_key('attempt') ) or csv_entry['attempt'] < attempt_number:
		csv_entry['file'] = file_name
		csv_entry['attempt'] = attempt_number


def attempt(filename):
	end_file_name = len(filename)-4
	return int(filename[end_file_name-2:end_file_name])

# Do stuff:

def copy_and_rename_files(output_folder, participant_id, csv_dictonaries):
	if not os.path.isdir(output_folder):
		os.mkdir(output_folder)

	current_output_folder = output_folder + '/' +  participant_id
	if not os.path.isdir(current_output_folder):
		os.mkdir(current_output_folder)
	for entry in csv_dictonaries:
		old_name = entry['file']
		new_name = current_output_folder + '/' + new_name_for_file(int(participant_id), entry)
		shutil.copy2(old_name, new_name)