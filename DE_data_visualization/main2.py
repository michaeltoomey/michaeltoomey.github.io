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

#Import and organize PWM and calling cards data
eds1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YBR033W.rank_scores.txt')
eds1_pwm_data.createGeneListFile('data_files/eds1_top_pwm_matches.txt')
eds1_cc_plus_lys_data = bindingdata.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.Eds1-Tagin+Lys_filtered.gnashy')
eds1_cc_plus_lys_data.createGeneListFile('data_files/eds1_top_cc_plusLys_matches.txt')
eds1_cc_minus_lys_data = bindingdata.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.Eds1-Tagin-Lys_filtered.gnashy')
eds1_cc_minus_lys_data.createGeneListFile('data_files/eds1_top_cc_minusLys_matches.txt')
utils.combineGeneLists('data_files/eds1_direct_binding_data.txt', ['data_files/eds1_top_cc_plusLys_matches.txt', 'data_files/eds1_top_cc_minusLys_matches.txt', 'data_files/eds1_top_pwm_matches.txt'])
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YBR033W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/eds1_direct_binding_data.txt'])

#Build data container
strainSys = 'YBR033W'
strainComm = 'EDS1'
base_strainSys = 'BY4741'
comparison = strainSys + 'vs' + base_strainSys
media = ['Glucose', 'Galactose']
cond_metadata = []

if 'Glucose' in media:
	sugar_content = ['Glucose'] * 6
	lys_content = ['NoLys'] * 6
	conds = timepoints
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, sugar, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, sugar, strainSys])
		cond_metadata += [metadata]

if 'Galactose' in media:
	sugar_content = ['Galactose'] * 2
	lys_content = ['NoLys'] + ['PlusLys']
	conds = ['Galactose.minusLys', 'Galactose.plusLys']
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, strainSys])
		cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/' + comparison + '_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/' + comparison + '_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')
data.combineConditions(['Galactose.minusLys', 'Galactose.plusLys'], 'Gal')

#Export data to files to be used by cytoscape.js network graphing library
networks[strainComm] = {}
networks[strainComm]['files'] = {}
network_dir = 'cytoscape_data/' + strainSys + '_networks/'
with open('gene_lists/' + strainSys + '_network_lists.txt', 'rb') as f:
	for line in f:
		network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
		filename = network_name.replace(' ', '') + '_' + comparison + '.json'
		gene_list = gene_list.split(',')
		networks[strainComm]['files'][network_name] = network_dir + filename
		data.writeToCytoscapeDataObj(strainSys, strainComm, gene_list, network_dir + filename)

networks[strainComm]['conds'] = cond_metadata

##### RGT1 vs. WT ######

#Import and organize PWM and calling cards data
rgt1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YKL038W.rank_scores.txt')
rgt1_pwm_data.createGeneListFile('data_files/rgt1_top_pwm_matches.txt')
rgt1_plus_cc_data = bindingdata.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.RGT1-Tagin+Lys_filtered.txt')
rgt1_plus_cc_data.createGeneListFile('data_files/rgt1_top_cc_plusLys_matches.txt')
rgt1_minus_cc_data = bindingdata.callingCardsDataProcesser('../../Raw Data Sets/NULL_model_results.RGT1-Tagin-Lys_filtered.txt')
rgt1_minus_cc_data.createGeneListFile('data_files/rgt1_top_cc_minusLys_matches.txt')
utils.combineGeneLists('data_files/rgt1_direct_binding_data.txt', ['data_files/rgt1_top_cc_plusLys_matches.txt', 'data_files/rgt1_top_cc_minusLys_matches.txt', 'data_files/rgt1_top_pwm_matches.txt'])
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YKL038W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/rgt1_direct_binding_data.txt'])

#Build data container
strainSys = 'YKL038W'
strainComm = 'RGT1'
base_strainSys = 'BY4741'
comparison = strainSys + 'vs' + base_strainSys
media = ['Glucose', 'Galactose']
cond_metadata = []

if 'Glucose' in media:
	sugar_content = ['Glucose'] * 6
	lys_content = ['NoLys'] * 6
	conds = timepoints
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, sugar, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, sugar, strainSys])
		cond_metadata += [metadata]

if 'Galactose' in media:
	sugar_content = ['Galactose'] * 2
	lys_content = ['NoLys'] + ['PlusLys']
	conds = ['Galactose.minusLys', 'Galactose.plusLys']
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, strainSys])
		cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/' + comparison + '_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/' + comparison + '_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')
data.combineConditions(['Galactose.minusLys', 'Galactose.plusLys'], 'Gal')

#Export data to files to be used by cytoscape.js network graphing library
networks[strainComm] = {}
networks[strainComm]['files'] = {}
network_dir = 'cytoscape_data/' + strainSys + '_networks/'
with open('gene_lists/' + strainSys + '_network_lists.txt', 'rb') as f:
	for line in f:
		network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
		filename = network_name.replace(' ', '') + '_' + comparison + '.json'
		gene_list = gene_list.split(',')
		networks[strainComm]['files'][network_name] = network_dir + filename
		data.writeToCytoscapeDataObj(strainSys, strainComm, gene_list, network_dir + filename)

networks[strainComm]['conds'] = cond_metadata

##### MIG1 vs. WT ######

#Import and organize PWM and calling cards data
mig1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YGL035C.rank_scores.txt')
mig1_pwm_data.createGeneListFile('data_files/mig1_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YGL035C_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/mig1_top_pwm_matches.txt'])

#Build data container
strainSys = 'YGL035C'
strainComm = 'MIG1'
base_strainSys = 'BY4741'
comparison = strainSys + 'vs' + base_strainSys
media = ['Glucose']
cond_metadata = []

if 'Glucose' in media:
	sugar_content = ['Glucose'] * 6
	lys_content = ['NoLys'] * 6
	conds = timepoints
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, sugar, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, sugar, strainSys])
		cond_metadata += [metadata]

if 'Galactose' in media:
	sugar_content = ['Galactose'] * 2
	lys_content = ['NoLys'] + ['PlusLys']
	conds = ['Galactose.minusLys', 'Galactose.plusLys']
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, strainSys])
		cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/' + comparison + '_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/' + comparison + '_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')

#Export EDS1/WT data to files to be used by cytoscape.js network graphing library
networks[strainComm] = {}
networks[strainComm]['files'] = {}
network_dir = 'cytoscape_data/' + strainSys + '_networks/'
with open('gene_lists/' + strainSys + '_network_lists.txt', 'rb') as f:
	for line in f:
		network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
		filename = network_name.replace(' ', '') + '_' + comparison + '.json'
		gene_list = gene_list.split(',')
		networks[strainComm]['files'][network_name] = network_dir + filename
		data.writeToCytoscapeDataObj(strainSys, strainComm, gene_list, network_dir + filename)

networks[strainComm]['conds'] = cond_metadata

##### MIG2 vs. WT ######

#Import and organize PWM and calling cards data
mig2_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YGL209W.rank_scores.txt')
mig2_pwm_data.createGeneListFile('data_files/mig2_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YGL209W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/mig2_top_pwm_matches.txt'])

#Build data container
strainSys = 'YGL209W'
strainComm = 'MIG2'
base_strainSys = 'BY4741'
comparison = strainSys + 'vs' + base_strainSys
media = ['Glucose']
cond_metadata = []

if 'Glucose' in media:
	sugar_content = ['Glucose'] * 6
	lys_content = ['NoLys'] * 6
	conds = timepoints
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, sugar, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, sugar, strainSys])
		cond_metadata += [metadata]

if 'Galactose' in media:
	sugar_content = ['Galactose'] * 2
	lys_content = ['NoLys'] + ['PlusLys']
	conds = ['Galactose.minusLys', 'Galactose.plusLys']
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, strainSys])
		cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/' + comparison + '_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/' + comparison + '_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')

#Export data to files to be used by cytoscape.js network graphing library
networks[strainComm] = {}
networks[strainComm]['files'] = {}
network_dir = 'cytoscape_data/' + strainSys + '_networks/'
with open('gene_lists/' + strainSys + '_network_lists.txt', 'rb') as f:
	for line in f:
		network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
		filename = network_name.replace(' ', '') + '_' + comparison + '.json'
		gene_list = gene_list.split(',')
		networks[strainComm]['files'][network_name] = network_dir + filename
		data.writeToCytoscapeDataObj(strainSys, strainComm, gene_list, network_dir + filename)

networks[strainComm]['conds'] = cond_metadata

##### SNF1 vs. WT ######

#Build data container
strainSys = 'YDR477W'
strainComm = 'SNF1'
base_strainSys = 'BY4741'
comparison = strainSys + 'vs' + base_strainSys
media = ['Glucose']
cond_metadata = []

if 'Glucose' in media:
	sugar_content = ['Glucose'] * 6
	lys_content = ['NoLys'] * 6
	conds = timepoints
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, sugar, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, sugar, strainSys])
		cond_metadata += [metadata]

if 'Galactose' in media:
	sugar_content = ['Galactose'] * 2
	lys_content = ['NoLys'] + ['PlusLys']
	conds = ['Galactose.minusLys', 'Galactose.plusLys']
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, strainSys])
		cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/' + comparison + '_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/' + comparison + '_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')

#Export data to files to be used by cytoscape.js network graphing library
networks[strainComm] = {}
networks[strainComm]['files'] = {}
network_dir = 'cytoscape_data/' + strainSys + '_networks/'
with open('gene_lists/' + strainSys + '_network_lists.txt', 'rb') as f:
	for line in f:
		network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
		filename = network_name.replace(' ', '') + '_' + comparison + '.json'
		gene_list = gene_list.split(',')
		networks[strainComm]['files'][network_name] = network_dir + filename
		data.writeToCytoscapeDataObj(strainSys, strainComm, gene_list, network_dir + filename)

networks[strainComm]['conds'] = cond_metadata

##### MIG1.MIG2 vs. WT ######

#Import and organize PWM and calling cards data
mig1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YGL035C.rank_scores.txt')
mig1_pwm_data.createGeneListFile('data_files/mig1_top_pwm_matches.txt')
mig2_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YGL209W.rank_scores.txt')
mig2_pwm_data.createGeneListFile('data_files/mig2_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YGL209W.YGL035C_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/mig2_top_pwm_matches.txt', 'data_files/mig1_top_pwm_matches.txt'])

#Build data container
strainSys = 'YGL209W.YGL035C'
strainComm = 'MIG2MIG1'
base_strainSys = 'BY4741'
comparison = strainSys + 'vs' + base_strainSys
media = ['Glucose']
cond_metadata = []

if 'Glucose' in media:
	sugar_content = ['Glucose'] * 6
	lys_content = ['NoLys'] * 6
	conds = timepoints
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, sugar, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, sugar, strainSys])
		cond_metadata += [metadata]

if 'Galactose' in media:
	sugar_content = ['Galactose'] * 2
	lys_content = ['NoLys'] + ['PlusLys']
	conds = ['Galactose.minusLys', 'Galactose.plusLys']
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, strainSys])
		cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/' + comparison + '_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json', target_lfc=1.0)
#Combine conditions into classes of interest
# data.saveDEData('processed_DE_data/' + comparison + '_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')

#Export data to files to be used by cytoscape.js network graphing library
networks[strainComm] = {}
networks[strainComm]['files'] = {}
network_dir = 'cytoscape_data/' + strainSys + '_networks/'
with open('gene_lists/' + strainSys + '_network_lists.txt', 'rb') as f:
	for line in f:
		network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
		filename = network_name.replace(' ', '') + '_' + comparison + '.json'
		gene_list = gene_list.split(',')
		networks[strainComm]['files'][network_name] = network_dir + filename
		data.writeToCytoscapeDataObj(strainSys, strainComm, gene_list, network_dir + filename)

networks[strainComm]['conds'] = cond_metadata


#Save metadata file
with open('cytoscape_data/file_metadata.json', 'wb') as f:
	json.dump(networks, f)


##### Mig1.Rgt1 vs. WT ######

#Import and organize PWM and calling cards data
mig1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YGL035C.rank_scores.txt')
mig1_pwm_data.createGeneListFile('data_files/mig1_top_pwm_matches.txt')
rgt1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YKL038W.rank_scores.txt')
rgt1_pwm_data.createGeneListFile('data_files/YKL038W_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YGL035C.YKL038W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/YKL038W_top_pwm_matches.txt', 'data_files/mig1_top_pwm_matches.txt'])

#Build data container
strainSys = 'YGL035C.YKL038W'
strainComm = 'MIG1RGT1'
base_strainSys = 'BY4741'
comparison = strainSys + 'vs' + base_strainSys
media = ['Glucose']
cond_metadata = []

if 'Glucose' in media:
	sugar_content = ['Glucose'] * 6
	lys_content = ['NoLys'] * 6
	conds = timepoints
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, sugar, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, sugar, strainSys])
		cond_metadata += [metadata]

if 'Galactose' in media:
	sugar_content = ['Galactose'] * 2
	lys_content = ['NoLys'] + ['PlusLys']
	conds = ['Galactose.minusLys', 'Galactose.plusLys']
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, strainSys])
		cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/' + comparison + '_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json', target_lfc=1.0)
# data.saveDEData('processed_DE_data/' + comparison + '_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')

#Export data to files to be used by cytoscape.js network graphing library
networks[strainComm] = {}
networks[strainComm]['files'] = {}
network_dir = 'cytoscape_data/' + strainSys + '_networks/'
with open('gene_lists/' + strainSys + '_network_lists.txt', 'rb') as f:
	for line in f:
		network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
		filename = network_name.replace(' ', '') + '_' + comparison + '.json'
		gene_list = gene_list.split(',')
		networks[strainComm]['files'][network_name] = network_dir + filename
		data.writeToCytoscapeDataObj(strainSys, strainComm, gene_list, network_dir + filename)

networks[strainComm]['conds'] = cond_metadata


#Save metadata file
with open('cytoscape_data/file_metadata.json', 'wb') as f:
	json.dump(networks, f)


##### Rgt1.Mig2 vs. WT ######

#Import and organize PWM and calling cards data
mig2_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YGL209W.rank_scores.txt')
mig2_pwm_data.createGeneListFile('data_files/mig1_top_pwm_matches.txt')
rgt1_pwm_data = bindingdata.PWMDataProcessor('../../Raw Data Sets/YKL038W.rank_scores.txt')
rgt1_pwm_data.createGeneListFile('data_files/YKL038W_top_pwm_matches.txt')
#Add binding data to edge index file
appended_info = appendedinformation.BuildAppendedGeneInformationFile(output_file='data_files/YKL038W.YGL209W_cytoscape_info_edges.json')
appended_info.addGeneInformationToFile('direct', [1], ['data_files/YKL038W_top_pwm_matches.txt', 'data_files/mig2_top_pwm_matches.txt'])

#Build data container
strainSys = 'YKL038W.YGL209W'
strainComm = 'RGT1MIG2'
base_strainSys = 'BY4741'
comparison = strainSys + 'vs' + base_strainSys
media = ['Glucose']
cond_metadata = []

if 'Glucose' in media:
	sugar_content = ['Glucose'] * 6
	lys_content = ['NoLys'] * 6
	conds = timepoints
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, sugar, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, sugar, strainSys])
		cond_metadata += [metadata]

if 'Galactose' in media:
	sugar_content = ['Galactose'] * 2
	lys_content = ['NoLys'] + ['PlusLys']
	conds = ['Galactose.minusLys', 'Galactose.plusLys']
	for cond, sugar, lys in zip(conds, sugar_content, lys_content):
		metadata = {'name': cond, 'vars': {'sugar': sugar, 'lys': lys}, 'files': {}}
		metadata['files']['edgeR'] = ff_edger.getFilePath([cond, base_strainSys, strainSys])
		metadata['files']['DESeq2'] = ff_deseq2.getFilePath([cond, base_strainSys, strainSys])
		cond_metadata += [metadata]

data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/' + comparison + '_comparisons.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json')
# data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/'+ strainSys +'_cytoscape_info_edges.json', target_lfc=1.0)
# data.saveDEData('processed_DE_data/' + comparison + '_comparisons.txt')
data.combineConditions(['T45', 'T60', 'T90', 'T180', 'T300'], 'HighGluc')
data.combineConditions(['Tneg1'], 'LowGluc')

#Export data to files to be used by cytoscape.js network graphing library
networks[strainComm] = {}
networks[strainComm]['files'] = {}
network_dir = 'cytoscape_data/' + strainSys + '_networks/'
with open('gene_lists/' + strainSys + '_network_lists.txt', 'rb') as f:
	for line in f:
		network_name, gene_list = line.replace('\n', '').replace('\r', '').split('\t')
		filename = network_name.replace(' ', '') + '_' + comparison + '.json'
		gene_list = gene_list.split(',')
		networks[strainComm]['files'][network_name] = network_dir + filename
		data.writeToCytoscapeDataObj(strainSys, strainComm, gene_list, network_dir + filename)

networks[strainComm]['conds'] = cond_metadata


#Save metadata file
with open('cytoscape_data/file_metadata.json', 'wb') as f:
	json.dump(networks, f)