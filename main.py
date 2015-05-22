import os, file_rename_utility, sys

cwd = os.getcwd()
data_folder =cwd + '/' + 'data'
csv_folder = cwd + '/' + 'id'
output_folder = cwd + '/' + 'output'

if len(sys.argv) > 1:
	data_folder = sys.argv[1]
if len(sys.argv) > 2:
	csv_folder = sys.argv[2]
if len(sys.argv) > 3:
	output_folder = sys.argv[3]

print "Looking for data in:\n\t%s" % data_folder
print "Looking for csv files in:\n\t%s" % csv_folder
print "Outputting new files in:\n\t%s" % output_folder

for folder in os.listdir(data_folder):
	participant_id = file_rename_utility.get_participant_id_from_folder(folder);
	print "Working on participant: " + participant_id
	csv_filename = "%s/%s.csv" % (csv_folder, participant_id)
	csv_dictonaries = file_rename_utility.generate_dictionary_from_csv_file(csv_filename)

	current_data_folder = data_folder + "/" + folder
	file_rename_utility.match_csv_dictionaries_to_files(csv_dictonaries, current_data_folder)

	file_rename_utility.copy_and_rename_files(output_folder, participant_id, csv_dictonaries)