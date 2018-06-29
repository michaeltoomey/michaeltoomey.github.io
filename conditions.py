import sys, os, json
import pandas as pd
import process_DE_Data as proc

class ConditionContainer():

	def __init__(self, condition_names, condition_files, program, conditions_sugar, conditions_lys, saved_data_file='', node_data_to_append='data_files/cytoscape_info_nodes.json', edge_data_to_append='data_files/cytoscape_info_edges.json', pval=0.05, lfc=2.0, direction='abs'):
		if program == 'DESeq2':
			self.pval_name = 'padj'
			self.lfc_name = 'log2FoldChange'
		else:
			self.pval_name = 'FDR'
			self.lfc_name = 'logFC'

		self.orfs = self.buildVerifiedORFsDict()
		self.info_to_append_nodes = self.buildInfoToAppendDict(node_data_to_append)
		self.info_to_append_edges = self.buildInfoToAppendDict(edge_data_to_append)

		self.conditions_sugar = {}
		for i, condition in enumerate(condition_names):
			self.conditions_sugar[condition] = conditions_sugar[i]

		self.conditions_lys = {}
		for i, condition in enumerate(condition_names):
			self.conditions_lys[condition] = conditions_lys[i]

		if saved_data_file:
			self.de_data = pd.read_csv(saved_data_file)
		else:
			data_list = []
			gene_list = []
			for file in condition_files:
				data = proc.DEDataProcessor(file, self.pval_name, self.lfc_name).genesLFCsPVals()
				data_list += [data]
				if gene_list:
					gene_list = list(set(gene_list) & set(data.index.values))
				else:
					gene_list = list(set(data.index.values))
			raw_data = pd.concat(data_list, keys=condition_names)

			idx = pd.IndexSlice
			self.de_data = pd.DataFrame(columns=condition_names)
			for gene in raw_data.index.levels[1].values:
				if gene in gene_list:
					gene_data = raw_data.loc[idx[:, gene], [self.lfc_name, self.pval_name]]
					processed_data = []
					for index, row in gene_data.iterrows():
						if direction == 'abs':
							if abs(row[self.lfc_name]) >= lfc and row[self.pval_name] < pval:
								processed_data += [row[self.lfc_name]]
							else:
								processed_data += [None]
						elif direction == 'act':
							if row[self.lfc_name] >= lfc and row[self.pval_name] < pval:
								processed_data += [row[self.lfc_name]]
							else:
								processed_data += [None]
						elif direction == 'repr':
							if row[self.lfc_name] <= -1 * lfc and row[self.pval_name] < pval:
								processed_data += [row[self.lfc_name]]
							else:
								processed_data += [None]

					if processed_data.count(None) != len(condition_names):
						self.de_data.loc[gene] = processed_data

	def combineConditions(self, conditions_to_combine, new_condition_name):
		sugar = []
		lys = []

		for condition in conditions_to_combine:
			sugar += [self.conditions_sugar[condition]]
			self.conditions_sugar.pop(condition)
			lys += [self.conditions_lys[condition]]
			self.conditions_lys.pop(condition)
		self.conditions_sugar[new_condition_name] = list(set(sugar))[0] if len(set(sugar)) == 1 else ''.join(set(sugar))
		self.conditions_lys[new_condition_name] = list(set(lys))[0] if len(set(lys)) == 1 else ''.join(set(lys))

		self.de_data[new_condition_name] = pd.concat([self.de_data[condition] for condition in conditions_to_combine], axis=1).mean(axis=1, numeric_only=True)
		self.de_data = self.de_data.drop(conditions_to_combine, axis=1)

	def removeCondition(self, condition):
		self.conditions_sugar.pop(condition)
		self.conditions_lys.pop(condition)
		self.de_data = self.de_data.drop(condition, axis=1)

	def writeToCytoscapeDataObj(self, sourceGene, gene_list, file_name):
		data = {}
		data['nodes'] = []
		data['edges'] = []
		counter = 1
		for index, row in self.de_data.iterrows():
			if index in gene_list:
				if index == sourceGene:
					continue
				else:
					gene_name = self.orfs[index] if index in self.orfs.keys() else index
					node_data = {'data': {'id': index, 'name': gene_name}}
					for key in self.info_to_append_nodes.keys():
							for subcategory in self.info_to_append_nodes[key].keys():
								if gene_name in self.info_to_append_nodes[key][subcategory]:
									if key in node_data['data'].keys():
										if node_data['data'][key] == None:
											node_data['data'][key] = subcategory
										else:
											node_data['data'][key] += subcategory
									else:
										node_data['data'][key] = subcategory
								else:
									node_data['data'][key] = None

					for condition in self.de_data.columns.values:
						if not pd.isna(row[condition]):
							interaction = 'represses' if row[condition] < 0 else 'activates'
							edge_data = {'data': {'id': sourceGene + index + condition,
													'source': sourceGene, 'target': index,
													'interaction': interaction,
													'lysInMedia':  self.conditions_lys[condition],
													'mediaSugar': self.conditions_sugar[condition],
													'condition': condition,
													'lfc': row[condition],
													'lit': 0,
													'manual': 0,
													'notes': None
												}
										}

							for key in self.info_to_append_edges.keys():
								for subcategory in self.info_to_append_edges[key].keys():
									if gene_name in self.info_to_append_edges[key][subcategory]:
										if key in edge_data['data'].keys():
											if edge_data['data'][key] == None:
												edge_data['data'][key] = subcategory
											else:
												edge_data['data'][key] += subcategory
										else:
											edge_data['data'][key] = subcategory
									else:
										edge_data['data'][key] = None

							data['edges'] += [edge_data]
							counter += 1
					data['nodes'] += [node_data]

		data['nodes'] += [{'data': {'id': sourceGene, 'metabolism': None, 'name': self.orfs[sourceGene]}}]

		with open(file_name, 'w') as f:
			json.dump(data, f, indent=5)
		f.close()

	def saveDEData(self, file_name):
		self.de_data.to_csv(file_name, sep='\t')

	def buildVerifiedORFsDict(self):
		orfs = pd.read_csv('../../Raw Data Sets/VerifiedORFs.csv', header=None, index_col=0, usecols=[1, 3])
		orfs_dict = orfs.to_dict()
		return orfs_dict[3]

	def buildInfoToAppendDict(self, file_name):
		if os.path.exists(file_name):
			with open(file_name, 'r') as f:
 				return json.load(f)
 			f.close()
		else:
			print 'No Appended Information File with That Path exists'
			return None