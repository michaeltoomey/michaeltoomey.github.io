import sys, os
import pandas as pd

class PWMDataProcessor():

	def __init__(self, filename):
		self.bindingSites = pd.read_csv(filename, sep='\t', header=None, names=['genes', 'pvals'])
		self.bindingSites = self.bindingSites.sort_values('pvals', ascending=True)

	def createGeneListFile(self, filename='data_files/top_pwm_matches.json'):
		self.bindingSites[:50].to_csv(filename, columns=['genes'], header=False, index=False)


class callingCardsDataProcesser():
	
	def __init__(self, filename):
		self.bindingSites = pd.read_csv(filename, sep='\t', header=None, names=[i for i in range(0, 12)])
		self.bindingSites = self.bindingSites.sort_values(7, ascending=True)

	def createGeneListFile(self, filename='data_files/top_cc_matches.json'):
		sites_to_write = self.bindingSites[self.bindingSites[7] <= 0.001]
		sites_to_write.to_csv(filename, columns=[1], header=False, index=False)


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