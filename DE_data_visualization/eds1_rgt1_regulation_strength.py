from scipy.stats import ks_2samp
from scipy.stats import anderson_ksamp
import sys, os, re, json
import matplotlib.pyplot as plt
import numpy as np
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

eds1_data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/YBR033WvsBY4741_comparisons_no_lfc.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YBR033W_cytoscape_info_edges.json')
# eds1_data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YBR033W_cytoscape_info_edges.json', target_lfc=0.0)
# eds1_data.saveDEData('processed_DE_data/eds1vsWT_comparisons_no_lfc.txt')


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

rgt1_data = conditions.ConditionContainer(cond_metadata, orfs, saved_data_file='processed_DE_data/YKL038WvsBY4741_comparisons_no_lfc.txt', node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YKL038W_cytoscape_info_edges.json')
# rgt1_data = conditions.ConditionContainer(cond_metadata, orfs, node_data='data_files/cytoscape_info_nodes.json', edge_data='data_files/YKL038W_cytoscape_info_edges.json', target_lfc=0.0)
# rgt1_data.saveDEData('processed_DE_data/rgt1vsWT_comparisons_no_lfc.txt')

### Histograms ###
eds1_low_gluc = eds1_data.de_data.iloc[:,0].dropna()
eds1_high_gluc = eds1_data.de_data.iloc[:,1].dropna()
# eds1_high_gluc = eds1_data.de_data.iloc[:,1:6].mean(axis=1).dropna()
eds1_gal = eds1_data.de_data.iloc[:,6:7].mean(axis=1).dropna()

rgt1_low_gluc = rgt1_data.de_data.iloc[:,0].dropna()
rgt1_high_gluc = rgt1_data.de_data.iloc[:,1].dropna()
# rgt1_high_gluc = rgt1_data.de_data.iloc[:,1:6].mean(axis=1).dropna()
rgt1_gal = rgt1_data.de_data.iloc[:,6:7].mean(axis=1).dropna()

low_comm = list(set(eds1_low_gluc.index.values) & set(rgt1_low_gluc.index.values))
high_comm = list(set(eds1_high_gluc.index.values) & set(rgt1_high_gluc.index.values))
gal_comm = list(set(eds1_gal.index.values) & set(rgt1_gal.index.values))

print 'Number of genes in low glucose:  ' + str(len(low_comm))
print 'Number of genes in high glucose: ' + str(len(high_comm))
print 'Number of genes in galactose   : ' + str(len(gal_comm))
print '\n\n\n'

bins = np.linspace(-4, 4, 200)

# plt.hist((rgt1_high_gluc[high_comm]).values, bins, label='RGT1 High Glucose')
# plt.hist((eds1_high_gluc[high_comm]).values, bins, label='EDS1 High Glucose')
# plt.hist((rgt1_gal[gal_comm]).values, bins, label='RGT1 Galactose')
# plt.hist((eds1_gal[gal_comm]).values, bins, label='EDS1 Galactose')
# plt.hist((eds1_low_gluc[low_comm]).values, bins, label='RGT1 Low Glucose')
# plt.hist((rgt1_low_gluc[low_comm]).values, bins, label='EDS1 Low Glucose')
# plt.legend(loc='upper right')
# plt.xlabel('Log2 Fold Change')
# plt.ylabel('Number of Genes')
# plt.title('LFCs of Genes Commonly Significantly DE Betweeen RGT1 and EDS1 Deletions in Three Different Conditions')
# plt.show()

eds1_low_gluc[low_comm].to_csv('lfc_statistical_tests_data/eds1_low_gluc_all.csv')
rgt1_low_gluc[low_comm].to_csv('lfc_statistical_tests_data/rgt1_low_gluc_all.csv')
eds1_high_gluc[high_comm].to_csv('lfc_statistical_tests_data/eds1_high_gluc_all.csv')
rgt1_high_gluc[high_comm].to_csv('lfc_statistical_tests_data/rgt1_high_gluc_all.csv')
eds1_gal[gal_comm].to_csv('lfc_statistical_tests_data/eds1_gal_all.csv')
rgt1_gal[gal_comm].to_csv('lfc_statistical_tests_data/rgt1_gal_all.csv')


print '***COMBINED DISTRIBUTIONS***'
print 'Low Gluc: ' + str(ks_2samp(eds1_low_gluc[low_comm], rgt1_low_gluc[low_comm]))
print 'Low Gluc: ' + str(anderson_ksamp([eds1_low_gluc[low_comm], rgt1_low_gluc[low_comm]]))
print '\n'
print 'High Gluc: ' + str(ks_2samp(eds1_high_gluc[high_comm], rgt1_high_gluc[high_comm]))
print 'High Gluc: ' + str(anderson_ksamp([eds1_high_gluc[high_comm], rgt1_high_gluc[high_comm]]))
print '\n'
print 'Gal: ' + str(ks_2samp(eds1_gal[gal_comm], rgt1_gal[gal_comm]))
print 'Gal: ' + str(anderson_ksamp([eds1_gal[gal_comm], rgt1_gal[gal_comm]]))	
print '\n\n\n'

###THIS ONE###
# plt.hist((rgt1_high_gluc[high_comm]).values, bins, label='rgt1_high_gluc', alpha=0.5)
# plt.hist((eds1_high_gluc[high_comm]).values, bins, label='eds1_high_gluc', alpha=0.5)
# plt.legend(loc='upper right')
# plt.show()

# plt.hist((rgt1_gal[gal_comm]).values, bins, label='rgt1_gal', alpha=0.5)
# plt.hist((eds1_gal[gal_comm]).values, bins, label='eds1_gal', alpha=0.5)
# plt.legend(loc='upper right')
# plt.show()

# plt.hist((rgt1_low_gluc[low_comm]).values, bins, label='rgt1_low_gluc', alpha=0.5)
# plt.hist((eds1_low_gluc[low_comm]).values, bins, label='eds1_low_gluc', alpha=0.5)
# plt.legend(loc='upper right')
# plt.show()

eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] < 0].to_csv('lfc_statistical_tests_data/eds1_low_gluc_neg.csv')
rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] < 0].to_csv('lfc_statistical_tests_data/rgt1_low_gluc_neg.csv')
eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] < 0].to_csv('lfc_statistical_tests_data/eds1_high_gluc_neg.csv')
rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] < 0].to_csv('lfc_statistical_tests_data/rgt1_high_gluc_neg.csv')
eds1_gal[gal_comm][eds1_gal[gal_comm] < 0].to_csv('lfc_statistical_tests_data/eds1_gal_neg.csv')
rgt1_gal[gal_comm][rgt1_gal[gal_comm] < 0].to_csv('lfc_statistical_tests_data/rgt1_gal_neg.csv')

print len(eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] < 0])
print len(rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] < 0])
print len(eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] < 0])
print len(rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] < 0])
print set(eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] < 0].index.values).symmetric_difference(set(rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] < 0].index.values))
print len(eds1_gal[gal_comm][eds1_gal[gal_comm] < 0])
print len(rgt1_gal[gal_comm][rgt1_gal[gal_comm] < 0])
print set(eds1_gal[gal_comm][eds1_gal[gal_comm] < 0].index.values).symmetric_difference(set(rgt1_gal[gal_comm][rgt1_gal[gal_comm] < 0].index.values))


print len(eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] > 0])
print len(rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] > 0])
print len(eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] > 0])
print len(rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] > 0])
print set(eds1_gal[gal_comm][eds1_gal[gal_comm] > 0].index.values).symmetric_difference(set(rgt1_gal[gal_comm][rgt1_gal[gal_comm] > 0].index.values))
print len(eds1_gal[gal_comm][eds1_gal[gal_comm] > 0])
print len(rgt1_gal[gal_comm][rgt1_gal[gal_comm] > 0])
print set(eds1_gal[gal_comm][eds1_gal[gal_comm] > 0].index.values).symmetric_difference(set(rgt1_gal[gal_comm][rgt1_gal[gal_comm] > 0].index.values))


print '***NEGATIVE LFCS ONLY***'
print 'Low Gluc: ' + str(ks_2samp(eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] < 0], rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] < 0]))
print 'Low Gluc: ' + str(anderson_ksamp([eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] < 0], rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] < 0]]))
print '\n'
print 'High Gluc: ' + str(ks_2samp(eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] < 0], rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] < 0]))
print 'High Gluc: ' + str(anderson_ksamp([eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] < 0], rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] < 0]]))
print '\n'
print 'Gal: ' + str(ks_2samp(eds1_gal[gal_comm][eds1_gal[gal_comm] < 0], rgt1_gal[gal_comm][rgt1_gal[gal_comm] < 0]))
print 'Gal: ' + str(anderson_ksamp([eds1_gal[gal_comm][eds1_gal[gal_comm] < 0], rgt1_gal[gal_comm][rgt1_gal[gal_comm] < 0]]))	
print '\n\n\n'

# plt.hist((rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] < 0]).values, bins, label='rgt1_high_gluc')
# plt.hist((eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] < 0]).values, bins, label='eds1_high_gluc')
# plt.hist((rgt1_gal[gal_comm][rgt1_gal[gal_comm] < 0]).values, bins, label='rgt1_gal')
# plt.hist((eds1_gal[gal_comm][eds1_gal[gal_comm] < 0]).values, bins, label='eds1_gal')
# plt.hist((eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] < 0]).values, bins, label='eds1_low_gluc')
# plt.hist((rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] < 0]).values, bins, label='rgt1_low_gluc')
# plt.legend(loc='upper right')

eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] > 0].to_csv('lfc_statistical_tests_data/eds1_low_gluc_pos.csv')
rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] > 0].to_csv('lfc_statistical_tests_data/rgt1_low_gluc_pos.csv')
eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] > 0].to_csv('lfc_statistical_tests_data/eds1_high_gluc_pos.csv')
rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] > 0].to_csv('lfc_statistical_tests_data/rgt1_high_gluc_pos.csv')
eds1_gal[gal_comm][eds1_gal[gal_comm] > 0].to_csv('lfc_statistical_tests_data/eds1_gal_pos.csv')
rgt1_gal[gal_comm][rgt1_gal[gal_comm] > 0].to_csv('lfc_statistical_tests_data/rgt1_gal_pos.csv')

print '***POSITIVE LFCS ONLY***'
print 'Low Gluc: ' + str(ks_2samp(eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] > 0], rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] > 0]))
print 'Low Gluc: ' + str(anderson_ksamp([eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] > 0], rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] > 0]]))
print '\n'
print 'High Gluc: ' + str(ks_2samp(eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] > 0], rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] > 0]))
print 'High Gluc: ' + str(anderson_ksamp([eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] > 0], rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] > 0]]))
print '\n'
print 'Gal: ' + str(ks_2samp(eds1_gal[gal_comm][eds1_gal[gal_comm] > 0], rgt1_gal[gal_comm][rgt1_gal[gal_comm] > 0]))
print 'Gal: ' + str(anderson_ksamp([eds1_gal[gal_comm][eds1_gal[gal_comm] > 0], rgt1_gal[gal_comm][rgt1_gal[gal_comm] > 0]]))	
print '\n\n\n'

# plt.hist((rgt1_high_gluc[high_comm][rgt1_high_gluc[high_comm] > 0]).values, bins, label='rgt1_high_gluc')
# plt.hist((eds1_high_gluc[high_comm][eds1_high_gluc[high_comm] > 0]).values, bins, label='eds1_high_gluc')
# plt.hist((rgt1_gal[gal_comm][rgt1_gal[gal_comm] > 0]).values, bins, label='rgt1_gal')
# plt.hist((eds1_gal[gal_comm][eds1_gal[gal_comm] > 0]).values, bins, label='eds1_gal')
# plt.hist((eds1_low_gluc[low_comm][eds1_low_gluc[low_comm] > 0]).values, bins, label='eds1_low_gluc')
# plt.hist((rgt1_low_gluc[low_comm][rgt1_low_gluc[low_comm] > 0]).values, bins, label='rgt1_low_gluc')
# plt.legend(loc='upper right')
# plt.show()