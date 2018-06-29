import sys, os, re, json
import conditions, appendedInformation, bindingData, findDEFiles

timepoints = ['Tneg1', 'T45', 'T60', 'T90', 'T180', 'T300']
networks = {}

#Build map for parsing and finding DE files
ff = findDEFiles.DifferentialExpressionFiles('../../DifferentialExpressionGeneSets/')
ff.buildDirectoryMap()

#Import and organize process-related data for annotating gene nodes
appended_info = appendedInformation.BuildAppendedGeneInformationFile(output_file='data_files/cytoscape_info_nodes.json')
#Add process-related data to node index file
appended_info.addGeneInformationToFile('metabolism', ['proGrowth', 'proResp'], ['data_files/pro_growth_genes.txt', 'data_files/pro_respiration_genes.txt'])
 

##### EDS1 vs. WT ######

#Import and organize Eds1 PWM and calling cards data
eds1_pwm_data = bindingData.PWMDataProcessor('../../Raw Data Sets/YBR033W.rank_scores.txt')
eds1_pwm_data.createGeneListFile('data_files/eds1_top_pwm_matches.txt')
eds1_cc_plus_lys_data = bindingData.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.Eds1-Tagin+Lys_filtered.gnashy')
eds1_cc_plus_lys_data.createGeneListFile('data_files/eds1_top_cc_plusLys_matches.txt')
eds1_cc_plus_lys_data = bindingData.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.Eds1-Tagin-Lys_filtered.gnashy')
eds1_cc_plus_lys_data.createGeneListFile('data_files/eds1_top_cc_minusLys_matches.txt')
bindingData.combineGeneLists('data_files/eds1_direct_binding_data.txt', ['data_files/eds1_top_cc_plusLys_matches.txt', 'data_files/eds1_top_cc_minusLys_matches.txt', 'data_files/eds1_top_pwm_matches.txt'])
#Add binding data to edge index file
appended_info = appendedInformation.BuildAppendedGeneInformationFile(output_file='data_files/YBR033W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/eds1_direct_binding_data.txt'])

#Obtain list of BY4741/EDS1 DE data files for chemostat samples
files = []
for tp in ['Tneg1', 'T45', 'T60', 'T90', 'T180', 'T300']:
	for strain in ['YBR033W']:
		files += [ff.getFilePath([tp, 'BY4741', 'Glucose', strain])]
#Obtain list of BY4741/EDS1 DE data files for calling cards-like samples
for media in ['Galactose.minusLys', 'Galactose.plusLys']:
	for strain in ['YBR033W']:
		files += [ff.getFilePath([media, 'BY4741', strain])]

#Build EDS1/WT data container
sugar = ['gluc'] * 6 + ['gal'] * 2
lys = ['nolys'] * 7 + ['lys']
cond = timepoints + ['galpluslys', 'galminuslys']
# data = conditions.ConditionContainer(timepoints, files, 'edgeR', sugar, lys, saved_data_file='processed_DE_data/test.csv', node_data_to_append='data_files/YBR033W_cytoscape_info_edges.json', edge_data_to_append='data_files/YBR033W_cytoscape_info_nodes.json', lfc=1.0)
data = conditions.ConditionContainer(cond, files, 'edgeR', sugar, lys, node_data_to_append='data_files/cytoscape_info_nodes.json', edge_data_to_append='data_files/YBR033W_cytoscape_info_edges.json', lfc=1.0)
#Combine conditions into classes of interest
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'highgluc')
data.combineConditions(['Tneg1'], 'lowgluc')
# data.saveDEData('processed_DE_data/eds1vsWT_comparisons.csv')

#Export EDS1/WT data to files to be used by cytoscape.js network graphing library
networks['YBR033W'] = {}
network_dir = 'cytoscape_data/YBR033W_networks/'
with open('gene_lists/eds1_network_lists.txt', 'r') as f:
	with open(network_dir + 'metadata.csv', 'w') as o:
		for line in f:
			network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
			filename = network_name.replace(' ', '') + '_eds1vsWT.json'
			gene_list = gene_list.split(',')
			networks['YBR033W'][network_name] = network_dir + filename
			data.writeToCytoscapeDataObj('YBR033W', gene_list, network_dir + filename)
			o.write(network_name + ',' + filename + '\n')
	o.close()
f.close()


##### RGT1 vs. WT ######

#Import and organize Rgt1 PWM and calling cards data
rgt1_pwm_data = bindingData.PWMDataProcessor('../../Raw Data Sets/YKL038W.rank_scores.txt')
rgt1_pwm_data.createGeneListFile('data_files/rgt1_top_pwm_matches.txt')
rgt1_cc_data = bindingData.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.RGT1-Tagin+Lys_filtered.txt')
rgt1_cc_data.createGeneListFile('data_files/rgt1_top_cc_plusLys_matches.txt')
rgt1_cc_data = bindingData.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.RGT1-Tagin-Lys_filtered.txt')
rgt1_cc_data.createGeneListFile('data_files/rgt1_top_cc_minusLys_matches.txt')
bindingData.combineGeneLists('data_files/rgt1_direct_binding_data.txt', ['data_files/rgt1_top_cc_plusLys_matches.txt', 'data_files/rgt1_top_cc_minusLys_matches.txt', 'data_files/rgt1_top_pwm_matches.txt'])
#Add binding data to edge index file
appended_info = appendedInformation.BuildAppendedGeneInformationFile(output_file='data_files/YKL038W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/rgt1_direct_binding_data.txt'])

#Obtain list of BY4741/YKL038W DE data files for chemostat samples
files = []
for tp in ['Tneg1', 'T45', 'T60', 'T90', 'T180', 'T300']:
	for strain in ['YKL038W']:
		files += [ff.getFilePath([tp, 'BY4741', 'Glucose', strain])]
#Obtain list of BY4741/EDS1 DE data files for calling cards-like samples
for media in ['Galactose.minusLys', 'Galactose.plusLys']:
	for strain in ['YKL038W']:
		files += [ff.getFilePath([media, 'BY4741', strain])]

#Build RGT1/WT data container
sugar = ['gluc'] * 6 + ['gal'] * 2
lys = ['nolys'] * 7 + ['lys']
cond = timepoints + ['galpluslys', 'galminuslys']
data = conditions.ConditionContainer(cond, files, 'edgeR', sugar, lys, node_data_to_append='data_files/cytoscape_info_nodes.json', edge_data_to_append='data_files/YKL038W_cytoscape_info_edges.json', lfc=1.0)
#Combine conditions into classes of interest
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'highgluc')
data.combineConditions(['Tneg1'], 'lowgluc')

#Export RGT1/WT data to files to be used by cytoscape.js network graphing library
networks['YKL038W'] = {}
network_dir = 'cytoscape_data/YKL038W_networks/'
with open('gene_lists/rgt1_network_lists.txt', 'r') as f:
	with open(network_dir + 'metadata.csv', 'w') as o:
		for line in f:
			network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
			filename = network_name.replace(' ', '') + '_rgt1vsWT.json'
			gene_list = gene_list.split(',')
			networks['YKL038W'][network_name] = network_dir + filename
			data.writeToCytoscapeDataObj('YKL038W', gene_list, network_dir + filename)
			o.write(network_name + ',' + filename + '\n')
	o.close()
f.close()


##### MIG1 vs. WT ######

#Import and organize Mig1 PWM and calling cards data
rgt1_pwm_data = bindingData.PWMDataProcessor('../../Raw Data Sets/YGL035C.rank_scores.txt')
rgt1_pwm_data.createGeneListFile('data_files/mig1_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedInformation.BuildAppendedGeneInformationFile(output_file='data_files/YGL035C_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/mig1_top_pwm_matches.txt'])

#Obtain list of BY4741/YGL035C DE data files for chemostat samples
files = []
for tp in ['Tneg1', 'T45', 'T60', 'T90', 'T180', 'T300']:
	for strain in ['YGL035C']:
		files += [ff.getFilePath([tp, 'BY4741', 'Glucose', strain])]

#Build MIG1/WT data container
sugar = ['gluc'] * 6
lys = ['nolys'] * 6
cond = timepoints
data = conditions.ConditionContainer(cond, files, 'edgeR', sugar, lys, node_data_to_append='data_files/cytoscape_info_nodes.json', edge_data_to_append='data_files/YGL035C_cytoscape_info_edges.json', lfc=1.0)
#Combine conditions into classes of interest
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'highgluc')
data.combineConditions(['Tneg1'], 'lowgluc')

#Export MIG1/WT data to files to be used by cytoscape.js network graphing library
networks['YGL035C'] = {}
network_dir = 'cytoscape_data/YGL035C_networks/'
with open('gene_lists/mig1_network_lists.txt', 'r') as f:
	with open(network_dir + 'metadata.csv', 'w') as o:
		for line in f:
			network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
			filename = network_name.replace(' ', '') + '_mig1vsWT.json'
			gene_list = gene_list.split(',')
			networks['YGL035C'][network_name] = network_dir + filename
			data.writeToCytoscapeDataObj('YGL035C', gene_list, network_dir + filename)
			o.write(network_name + ',' + filename + '\n')
	o.close()
f.close()


##### MIG2 vs. WT ######

#Import and organize Mig2 PWM and calling cards data
rgt1_pwm_data = bindingData.PWMDataProcessor('../../Raw Data Sets/YGL209W.rank_scores.txt')
rgt1_pwm_data.createGeneListFile('data_files/mig2_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedInformation.BuildAppendedGeneInformationFile(output_file='data_files/YGL209W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/mig2_top_pwm_matches.txt'])

#Obtain list of BY4741/YGL209W DE data files for chemostat samples
files = []
for tp in ['Tneg1', 'T45', 'T60', 'T90', 'T180', 'T300']:
	for strain in ['YGL209W']:
		files += [ff.getFilePath([tp, 'BY4741', 'Glucose', strain])]

#Build MIG1/WT data container
sugar = ['gluc'] * 6
lys = ['nolys'] * 6
cond = timepoints
data = conditions.ConditionContainer(cond, files, 'edgeR', sugar, lys, node_data_to_append='data_files/cytoscape_info_nodes.json', edge_data_to_append='data_files/YGL209W_cytoscape_info_edges.json', lfc=1.0)
#Combine conditions into classes of interest
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'highgluc')
data.combineConditions(['Tneg1'], 'lowgluc')

#Export MIG1/WT data to files to be used by cytoscape.js network graphing library
networks['YGL209W'] = {}
network_dir = 'cytoscape_data/YGL209W_networks/'
with open('gene_lists/mig2_network_lists.txt', 'r') as f:
	with open(network_dir + 'metadata.csv', 'w') as o:
		for line in f:
			network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
			filename = network_name.replace(' ', '') + '_mig2vsWT.json'
			gene_list = gene_list.split(',')
			networks['YGL209W'][network_name] = network_dir + filename
			data.writeToCytoscapeDataObj('YGL209W', gene_list, network_dir + filename)
			o.write(network_name + ',' + filename + '\n')
	o.close()
f.close()

with open('cytoscape_data/file_metadata.json', 'w') as f:
	json.dump(networks, f)
f.close()