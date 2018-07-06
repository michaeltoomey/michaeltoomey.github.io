import sys, os, re, json
import conditions, appendedinformation, bindingdata, finddefiles, utils

timepoints = ['Tneg1', 'T45', 'T60', 'T90', 'T180', 'T300']
networks = {}
orfs = utils.buildVerifiedORFsDict()

#Build map for parsing and finding DE files
ff_edger = finddefiles.DifferentialExpressionFiles('raw_de_data/edger/')
ff_edger.buildDirectoryMap()

ff_deseq2 = finddefiles.DifferentialExpressionFiles('raw_de_data/deseq2/')
ff_deseq2.buildDirectoryMap()
#Import and organize process-related data for annotating gene nodes
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/cytoscape_info_nodes.json')
#Add process-related data to node index file
appended_info.addGeneInformationToFile('metabolism', ['proGrowth', 'proResp'], ['data_files/pro_growth_genes.txt', 'data_files/pro_respiration_genes.txt'])
 

##### EDS1 vs. WT ######

#Import and organize Eds1 PWM and calling cards data
eds1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YBR033W.rank_scores.txt')
eds1_pwm_data.createGeneListFile('data_files/eds1_top_pwm_matches.txt')
eds1_cc_plus_lys_data = bindingdata.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.Eds1-Tagin+Lys_filtered.gnashy')
eds1_cc_plus_lys_data.createGeneListFile('data_files/eds1_top_cc_plusLys_matches.txt')
eds1_cc_plus_lys_data = bindingdata.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.Eds1-Tagin-Lys_filtered.gnashy')
eds1_cc_plus_lys_data.createGeneListFile('data_files/eds1_top_cc_minusLys_matches.txt')
utils.combineGeneLists('data_files/eds1_direct_binding_data.txt', ['data_files/eds1_top_cc_plusLys_matches.txt', 'data_files/eds1_top_cc_minusLys_matches.txt', 'data_files/eds1_top_pwm_matches.txt'])
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YBR033W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/eds1_direct_binding_data.txt'])

#Build EDS1/WT data container
strain = 'YBR033W'
cond_metadata = []

sugar_content = ['Glucose'] * 6
lys_content = ['NoLys'] * 6
conds = timepoints
for cond, sugar, lys in zip(conds, sugar_content, lys_content):
	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', sugar, strain])
	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', sugar, strain])
	cond_metadata += [metadata]

sugar_content = ['Galactose'] * 2
lys_content = ['NoLys'] + ['PlusLys']
conds = ['Galactose.minusLys', 'Galactose.plusLys']
for cond, sugar, lys in zip(conds, sugar_content, lys_content):
	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', strain])
	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', strain])
	cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/eds1vsWT_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YBR033W_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YBR033W_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/eds1vsWT_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')
data.combineConditions(['Galactose.minusLys', 'Galactose.plusLys'], 'Gal')

#Export EDS1/WT data to files to be used by cytoscape.js network graphing library
networks[strain] = {}
network_dir = 'cytoscape_data/YBR033W_networks/'
with open('gene_lists/eds1_network_lists.txt', 'r') as f:
	with open(network_dir + 'metadata.csv', 'w') as o:
		for line in f:
			network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
			filename = network_name.replace(' ', '') + '_eds1vsWT.json'
			gene_list = gene_list.split(',')
			networks[strain][network_name] = network_dir + filename
			data.writeToCytoscapeDataObj(strain, gene_list, network_dir + filename)
			o.write(network_name + ',' + filename + '\n')
	o.close()
f.close()


##### RGT1 vs. WT ######

#Import and organize Rgt1 PWM and calling cards data
rgt1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YKL038W.rank_scores.txt')
rgt1_pwm_data.createGeneListFile('data_files/rgt1_top_pwm_matches.txt')
rgt1_cc_data = bindingdata.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.RGT1-Tagin+Lys_filtered.txt')
rgt1_cc_data.createGeneListFile('data_files/rgt1_top_cc_plusLys_matches.txt')
rgt1_cc_data = bindingdata.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.RGT1-Tagin-Lys_filtered.txt')
rgt1_cc_data.createGeneListFile('data_files/rgt1_top_cc_minusLys_matches.txt')
utils.combineGeneLists('data_files/rgt1_direct_binding_data.txt', ['data_files/rgt1_top_cc_plusLys_matches.txt', 'data_files/rgt1_top_cc_minusLys_matches.txt', 'data_files/rgt1_top_pwm_matches.txt'])
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YKL038W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/rgt1_direct_binding_data.txt'])

#Build RGT1/WT data container
strain = 'YKL038W'
cond_metadata = []

sugar_content = ['Glucose'] * 6
lys_content = ['NoLys'] * 6
conds = timepoints
for cond, sugar, lys in zip(conds, sugar_content, lys_content):
	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', sugar, strain])
	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', sugar, strain])
	cond_metadata += [metadata]

sugar_content = ['Galactose'] * 2
lys_content = ['NoLys'] + ['PlusLys']
conds = ['Galactose.minusLys', 'Galactose.plusLys']
for cond, sugar, lys in zip(conds, sugar_content, lys_content):
	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', strain])
	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', strain])
	cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/rgt1vsWT_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YKL038W_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YKL038W_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/rgt1vsWT_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')
data.combineConditions(['Galactose.minusLys', 'Galactose.plusLys'], 'Gal')


#Export RGT1/WT data to files to be used by cytoscape.js network graphing library
networks[strain] = {}
network_dir = 'cytoscape_data/YKL038W_networks/'
with open('gene_lists/rgt1_network_lists.txt', 'r') as f:
	with open(network_dir + 'metadata.csv', 'w') as o:
		for line in f:
			network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
			filename = network_name.replace(' ', '') + '_rgt1vsWT.json'
			gene_list = gene_list.split(',')
			networks[strain][network_name] = network_dir + filename
			data.writeToCytoscapeDataObj(strain, gene_list, network_dir + filename)
			o.write(network_name + ',' + filename + '\n')
	o.close()
f.close()


##### MIG1 vs. WT ######

#Import and organize Mig1 PWM and calling cards data
mig1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YGL035C.rank_scores.txt')
mig1_pwm_data.createGeneListFile('data_files/mig1_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YGL035C_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/mig1_top_pwm_matches.txt'])

#Build MIG1/WT data container
strain = 'YGL035C'
cond_metadata = []

sugar_content = ['Glucose'] * 6
lys_content = ['NoLys'] * 6
conds = timepoints
for cond, sugar, lys in zip(conds, sugar_content, lys_content):
	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', sugar, strain])
	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', sugar, strain])
	cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/mig1vsWT_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YGL035C_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YGL035C_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/mig1vsWT_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')

#Export MIG1/WT data to files to be used by cytoscape.js network graphing library
networks[strain] = {}
network_dir = 'cytoscape_data/YGL035C_networks/'
with open('gene_lists/mig1_network_lists.txt', 'r') as f:
	with open(network_dir + 'metadata.csv', 'w') as o:
		for line in f:
			network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
			filename = network_name.replace(' ', '') + '_mig1vsWT.json'
			gene_list = gene_list.split(',')
			networks[strain][network_name] = network_dir + filename
			data.writeToCytoscapeDataObj(strain, gene_list, network_dir + filename)
			o.write(network_name + ',' + filename + '\n')
	o.close()
f.close()


##### MIG2 vs. WT ######

#Import and organize Mig2 PWM and calling cards data
mig2_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YGL209W.rank_scores.txt')
mig2_pwm_data.createGeneListFile('data_files/mig2_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YGL209W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/mig2_top_pwm_matches.txt'])

#Build MIG2/WT data container
strain = 'YGL209W'
cond_metadata = []

sugar_content = ['Glucose'] * 6
lys_content = ['NoLys'] * 6
conds = timepoints
for cond, sugar, lys in zip(conds, sugar_content, lys_content):
	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', sugar, strain])
	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', sugar, strain])
	cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/mig2vsWT_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YGL209W_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YGL209W_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/mig2vsWT_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')

#Export MIG2/WT data to files to be used by cytoscape.js network graphing library
networks[strain] = {}
network_dir = 'cytoscape_data/YGL209W_networks/'
with open('gene_lists/mig2_network_lists.txt', 'r') as f:
	with open(network_dir + 'metadata.csv', 'w') as o:
		for line in f:
			network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
			filename = network_name.replace(' ', '') + '_mig2vsWT.json'
			gene_list = gene_list.split(',')
			networks[strain][network_name] = network_dir + filename
			data.writeToCytoscapeDataObj(strain, gene_list, network_dir + filename)
			o.write(network_name + ',' + filename + '\n')
	o.close()
f.close()


##### SNF1 vs. WT ######

# strain = 'YDR477W'
# cond_metadata = []

# sugar_content = ['Glucose'] * 6
# lys_content = ['NoLys'] * 6
# conds = timepoints
# for cond, sugar, lys in zip(conds, sugar_content, lys_content):
# 	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
# 	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', sugar, strain])
# 	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', sugar, strain])
# 	cond_metadata += [metadata]

# # data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/mig2vsWT_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json')
# snf1_data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', target_lfc=1.0)
# #Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/snf1vsWT_comparisons.txt')


# ##### YBR033W.YKL038W vs. WT ######

# strain = 'YDR477W'
# cond_metadata = []

# sugar_content = ['Glucose'] * 6
# lys_content = ['NoLys'] * 6
# conds = timepoints
# for cond, sugar, lys in zip(conds, sugar_content, lys_content):
# 	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
# 	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', sugar, strain])
# 	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', sugar, strain])
# 	cond_metadata += [metadata]

# # data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/mig2vsWT_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json')
# eds1rgt1_data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', target_lfc=1.0)
# #Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/eds1.rgt1vsWT_comparisons.txt')


# ##### MIG1.MIG2 vs. WT ######

# strain = 'YGL209W.YGL035C'
# cond_metadata = []

# sugar_content = ['Glucose'] * 6
# lys_content = ['NoLys'] * 6
# conds = timepoints
# for cond, sugar, lys in zip(conds, sugar_content, lys_content):
# 	metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
# 	metadata['files']['edgeR'] = ff_edger.getFilePath([cond, 'BY4741', sugar, strain])
# 	metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, 'BY4741', sugar, strain])
# 	cond_metadata += [metadata]

# # data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/mig2vsWT_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json')
# mig2mig1_data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', target_lfc=1.0)
# #Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/mig2.mig1vsWT_comparisons.txt')