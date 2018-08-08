import sys, os, csv
import pandas as pd
import numpy as np
import utils

orfs = utils.buildVerifiedORFsDict()

eds1_data = pd.read_csv("processed_DE_data/YBR033WvsBY4741_comparisons.txt", sep='\t', index_col=0)
eds1_data = eds1_data.loc[np.intersect1d(eds1_data.index.values, orfs.keys())]
rgt1_data = pd.read_csv("processed_DE_data/YKL038WvsBY4741_comparisons.txt", sep='\t', index_col=0)
rgt1_data = rgt1_data.loc[np.intersect1d(rgt1_data.index.values, orfs.keys())]

#dif wrt rgt1 = (dif in eds1 but not in rgt1 across any condition) || (dif in eds1 in opp dir from rgt1 in all dir)
unique_eds1_genes = set(eds1_data.index.values).difference(set(rgt1_data.index.values))
unique_eds1_data = eds1_data.loc[unique_eds1_genes]
data_of_int = unique_eds1_data[unique_eds1_data.isnull().sum(axis=1) < 4]
# print data_of_int
# print data_of_int.shape
genes_of_int = []
for gene in data_of_int.index.values:
	genes_of_int += [orfs[gene]]
print data_of_int.index.values
print genes_of_int
print unique_eds1_data.shape

# with open("diff_wrt_rgt1.csv", "w") as output:
#     writer = csv.writer(output, lineterminator='\n')
#     for gene in data_of_int.index.values:
#         writer.writerow([gene])

comm_genes = set(eds1_data.index.values).intersection(set(rgt1_data.index.values))
print len(comm_genes)
eds1_opp_dir = {}
rgt1_opp_dir = {}
for gene in comm_genes:
	eds1 = eds1_data.loc[gene]
	eds1.dropna(inplace=True)
	rgt1 = rgt1_data.loc[gene]
	rgt1.dropna(inplace=True)

	if eds1.size > 0 and rgt1.size > 0:
		comm_conds = set(eds1.index.values).intersection(set(rgt1.index.values))
		for cond in comm_conds:
			if eds1.loc[cond] * rgt1.loc[cond] < 0:
				if eds1.name in eds1_opp_dir.keys():
					eds1_opp_dir[eds1.name][cond] = eds1.loc[cond]
				else: 
					eds1_opp_dir[eds1.name] = {}
					eds1_opp_dir[eds1.name][cond] = eds1.loc[cond]

				if rgt1.name in rgt1_opp_dir.keys():
					rgt1_opp_dir[rgt1.name][cond] = rgt1.loc[cond]
				else: 
					rgt1_opp_dir[rgt1.name] = {}
					rgt1_opp_dir[rgt1.name][cond] = rgt1.loc[cond]


				# eds1_opp_dir[eds1.name] = [cond, eds1.loc[cond]]
				# eds1_opp_dir[rgt1.name] = [cond, rgt1.loc[cond]]

print eds1_opp_dir.keys()
genes_of_int = []
for gene in eds1_opp_dir.keys():
	genes_of_int += [orfs[gene]]
print genes_of_int
