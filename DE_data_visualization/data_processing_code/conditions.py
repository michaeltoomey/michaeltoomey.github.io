import sys, os, json, utils
import pandas as pd
import numpy as np
import processdedata as proc

class ConditionContainer():

	def __init__(self, condition_metadata, orfs, set_op='union', saved_data_file='', node_data=None, edge_data=None, target_pval=0.05, target_lfc=2.0, direction='abs'):
		self.condition_metadata = condition_metadata
		self.conditions = [condition['name'] for condition in condition_metadata]
		self.orfs = orfs
		self.node_data_dict = utils.buildInfoToAppendDict(node_data) if node_data else None
		self.edge_data_dict = utils.buildInfoToAppendDict(edge_data) if edge_data else None
		self.pval = {'edgeR': 'FDR', 'DESeq2': 'padj'}
		self.lfc = {'edgeR': 'logFC', 'DESeq2': 'log2FoldChange'}

		if saved_data_file:
			self.de_data = pd.read_csv(saved_data_file, sep='\t', index_col=0)
		else:
			raw_data_list = []
			gene_list = []
			for cond in self.condition_metadata:
				cond_data = []
				keys = []
				for program in cond['files'].keys():
					prog_data = proc.DEDataProcessor(cond['files'][program], self.pval[program], self.lfc[program]).genesLFCsPVals()
					cond_data += [prog_data]
					keys += list(prog_data.columns.values)

					if gene_list:
						gene_list = list(set(gene_list) & set(prog_data.index.values))
					else:
						gene_list = list(set(prog_data.index.values))
				raw_data_list += [pd.concat(cond_data, keys=cond['files'].keys())]
			raw_data = pd.concat(raw_data_list, keys=self.conditions)

			idx = pd.IndexSlice
			self.de_data = pd.DataFrame(columns=[condition['name'] for condition in self.condition_metadata])
			for gene in raw_data.index.levels[2].values:
				if gene in gene_list:
					gene_data = raw_data.loc[idx[:, :, gene], ['lfc', 'pval']]
					processed_data = []
					for cond in gene_data.index.levels[0].values:
						gene_cond_data = gene_data.loc[idx[cond]]
						processed_data += [self.extractLFC(gene_cond_data, 'intersection', target_pval, target_lfc, idx)]

					if processed_data.count(None) != len(self.conditions):
						self.de_data.loc[gene] = processed_data

	def extractLFC(self, gene_condition_data, set_op, target_pval, target_lfc, idx):
		lfc = []
		for program in gene_condition_data.index.levels[0]:
			prog_data = gene_condition_data.loc[idx[program]]

			gene_pval = prog_data.at[prog_data.index.values[0], 'pval']
			gene_lfc = prog_data.at[prog_data.index.values[0], 'lfc']
			if gene_pval < target_pval and abs(gene_lfc) > target_lfc:
				lfc += [gene_lfc]
		if lfc:
			if set_op == 'intersection':
				if len(lfc) == 2:
					return np.mean(lfc)
			else:
				return np.mean(lfc)
		return None


	def combineConditions(self, conditions_to_combine, new_condition_name):
		vars_dict = {}
		for cond in conditions_to_combine:
			for meta in self.condition_metadata:
				if meta['name'] == cond:
					for var in meta['vars'].keys():
						if var in vars_dict:
							vars_dict[var] += [meta['vars'][var]]
						else:
							vars_dict[var] = [meta['vars'][var]]
					self.condition_metadata.remove(meta)

		for var in vars_dict.keys():
			vars_dict[var] = list(set(vars_dict[var]))[0] if len(set(vars_dict[var])) == 1 else ''.join(set(vars_dict[var]))

		self.condition_metadata += [{'name': new_condition_name, 'vars': vars_dict}]

		self.de_data[new_condition_name] = pd.concat([self.de_data[condition] for condition in conditions_to_combine], axis=1).mean(axis=1, numeric_only=True)
		self.de_data = self.de_data.drop(conditions_to_combine, axis=1)

	def removeCondition(self, condition):
		self.conditions_sugar.pop(condition)
		self.conditions_lys.pop(condition)
		self.de_data = self.de_data.drop(condition, axis=1)

	def writeToCytoscapeDataObj(self, sourceGeneSystematic, sourceGeneCommon, gene_list, file_name):
		data = {}
		data['nodes'] = []
		data['edges'] = []
		counter = 1
		for index, row in self.de_data.iterrows():
			if index in gene_list:
				if index == sourceGeneSystematic:
					continue
				else:
					gene_name = self.orfs[index] if index in self.orfs.keys() else index
					node_data = {'data': {'id': index, 'name': gene_name}}
					if self.node_data_dict:
						for key in self.node_data_dict.keys():
								for subcategory in self.node_data_dict[key].keys():
									if gene_name in self.node_data_dict[key][subcategory]:
										if key in node_data['data'].keys():
											if node_data['data'][key] == None:
												node_data['data'][key] = subcategory
											else:
												node_data['data'][key] += subcategory
										else:
											node_data['data'][key] = subcategory
									else:
										node_data['data'][key] = None

					for cond in self.de_data.columns.values:
						lys = ''
						sugar = ''
						for cond_meta in self.condition_metadata:
							if cond_meta['name'] == cond:
								lys = cond_meta['vars']['lys']
								sugar = cond_meta['vars']['sugar']
						if not pd.isna(row[cond]):
							interaction = 'represses' if row[cond] > 0 else 'activates'
							edge_data = {'data': {'id': sourceGeneSystematic + index + cond,
													'source': sourceGeneSystematic, 'target': index,
													'interaction': interaction,
													'lysInMedia': lys,
													'mediaSugar': sugar,
													'condition': cond,
													'lfc': row[cond],
													'lit': 0,
													'manual': 0,
													'notes': None
												}
										}
							if self.edge_data_dict:

								for key in self.edge_data_dict.keys():
									for subcategory in self.edge_data_dict[key].keys():
										if gene_name == 'CNS1':
											print 'SHAKA WHEN THE WALLS FELL'
										if (gene_name in self.edge_data_dict[key][subcategory] or index in self.edge_data_dict[key][subcategory]):
											if gene_name == 'CNS1':
												print 'SHAKA WHEN THE WALLS FELL'
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

		data['nodes'] += [{'data': {'id': sourceGeneSystematic, 'metabolism': None, 'name': sourceGeneCommon}}]

		with open(file_name, 'w') as f:
			json.dump(data, f, indent=5)

	def saveDEData(self, file_name):
		self.de_data.to_csv(file_name, sep='\t')