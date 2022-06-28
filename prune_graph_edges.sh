#!/bin/bash

: << 'DESCRIPTION'
Prune edges from re-assembled graph to simplify the initial strain problem
DESCRIPTION

# $1: Assembly graph (GFA, 4 components- header (edges), segments, links (connections), paths (contigs)))
# $2: Edge metadata CSV [id,length,contigs,reads,coverage_contigs,coverage_reads]

# Split GFA file according to value in first column
awk -F"\t" '{outfile=($1 ".tsv") ; print $0 >>outfile ; close(outfile)}' < $1

# Prune edges (and associated links and paths) that are too short or too high-coverage
python prune_graph_edges.py $2

# Re-combine the pruned files to make a new graph file
PREFIX=`basename $2 .csv`
NEW_S="S_pruned_${PREFIX}.tsv"
NEW_L="L_pruned_${PREFIX}.tsv"
NEW_P="P_pruned_${PREFIX}.tsv"
cat 'H.tsv' $NEW_S $NEW_L $NEW_P > ${PREFIX}.gfa