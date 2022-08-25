from os.path import basename, join
import pandas as pd
import sys

'''
Prune edges from re-assembled graph to simplify the initial strain problem 
'''

# sys.argv[1]: Edge metadata CSV [id,length,contigs,reads,coverage_contigs,coverage_reads]

# Extract edges to keep 
edge_df = pd.read_csv(sys.argv[1], header = 0, sep = ';')
edge_nums = list(edge_df['id'])
edge_lst = ['edge_' + str(i) for i in edge_nums]
prefix = join(*basename(sys.argv[1]).split('.')[:-1])

# Make the segment and link components
s_df = pd.read_csv('S.tsv', header = None, sep = '\t')
s_out = s_df[s_df[1].isin(edge_lst)]
s_out.to_csv('S_pruned_' + prefix + '.tsv', header = False, index = False, sep = '\t')

l_df = pd.read_csv('L.tsv', header = None, sep = '\t')
l_int = l_df[l_df[1].isin(edge_lst)]
l_out = l_int[l_int[3].isin(edge_lst)]
l_out.to_csv('L_pruned_' + prefix + '.tsv', header = False, index = False, sep = '\t')

# Extract contigs to keep
# ctgs = list(edge_df['contigs'])
# ctg_lst = []
# for c in ctgs:
# 	tmp = c.replace('"', '').replace('\'', '').replace('[', ''). replace(']', '').split(', ')
# 	ctg_lst.extend(tmp)

def remove_edges(row, lst):
	edges = row[2].split(',')
	to_keep = []
	for edge in edges:
		tmp = edge
		if tmp.replace('+', '').replace('-', '') in lst:
			to_keep.append(edge)
	if len(to_keep) > 1:
		row[2] = ','.join(to_keep)
		return row
	else:
		return

# Make the path (contig) components
p_df = pd.read_csv('P.tsv', header = None, sep = '\t') # P contig_X edge_Y,edge_Z,etc. *
p_pruned = p_df.apply(lambda row : remove_edges(row, edge_lst), axis = 1)
p_pruned.dropna(how = 'all', inplace = True)
# p_out = p_df[p_df[1].isin(ctg_lst)]
p_pruned.to_csv('P_pruned_' + prefix + '.tsv', header = False, index = False, sep = '\t')
