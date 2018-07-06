import pandas as pd

class Utils():

	def buildVerifiedORFsDict(self):
		orfs = pd.read_csv('../../Raw Data Sets/VerifiedORFs.csv', header=None, index_col=0, usecols=[1, 3])
		orfs_dict = orfs.to_dict()
		return orfs_dict[3]

	def buildInfoToAppendDict(self, file_name):
		if os.path.exists(file_name):
			with open(file_name, 'r') as f:
					return json.load(f)
		else:
			print 'No Appended Information File with That Path exists'
			return None

	def combineGeneLists(filename, files_to_combine):
		gene_list = []
		for file in files_to_combine:
			with open(file, 'r') as f:
				for line in f:
					line = line.strip()
					gene_list += [line]

		with open(filename, 'w') as f:
			for item in gene_list:
				f.write(item + '\n')