import sys, os
import pandas as pd

class DEDataProcessor():

	def __init__(self, de_data_file, pval_name, lfc_name):
		self.de_data = pd.read_csv(de_data_file, index_col=0, sep='\t')

		self.pval_name = pval_name
		self.lfc_name = lfc_name

	def filterByPVal(self, pval=0.05):
		self.de_data = self.de_data[self.de_data[self.pval_name] < pval]

	def filterByLFC(self, lfc=2.0, direction='abs'):
		lfc_abs = abs(lfc)
		if direction == 'abs':
			self.de_data = self.de_data[self.de_data[self.lfc_name].abs() > lfc_abs]
		elif direction == 'act':
			repressed_data = self.de_data[self.de_data[self.lfc_name] < 0]
			self.de_data = repressed_data[repressed_data[self.lfc_name] < -1 * lfc_abs]
		elif direction == 'repr':
			activated_data = self.de_data[self.de_data[self.lfc_name] > 0]
			self.de_data = activated_data[activated_data[self.lfc_name] > lfc_abs]

	def genesLFCsPVals(self):
		lfc_pval_data = self.de_data[[self.lfc_name, self.pval_name]]
		lfc_pval_data.columns = ['lfc', 'pval']
		return lfc_pval_data

	def reset(self):
		self.de_data = self.raw_de_data