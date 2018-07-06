import sys, os, json

class BuildAppendedGeneInformationFile():

	def __init__(self, output_file='data_files/cytoscape_info.json'):
		self.output_file = output_file

	def addGeneInformationToFile(self, header, subcategories, information_files):
		added_info = {}
		if os.path.exists(self.output_file):
			with open(self.output_file) as f:
				added_info = json.load(f)
			f.close()

		added_info[header] = {}
		for subcategory, file in zip(subcategories, information_files):
			added_info[header][subcategory] = []

			with open(file, 'r') as f:
				for line in f:
					line = line.strip()
					added_info[header][subcategory] += [line]
			f.close()

		with open(self.output_file, 'w') as f:
			json.dump(added_info, f)
		f.close()

	def resetFile(self):
		if os.path.exists(self.output_file):
			os.remove(self.output_file)