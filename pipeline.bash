#! /bin/bash -l

#SBATCH --partition=panda
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=pipeline

conda activate

#! /athena/ihlab/scratch/bes4014/mambaforge-pypy3/bin/GraphAligner -g /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa -f /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis.fastq -a /athena/ihlab/scratch/bes4014/reads.gaf -x dbg
#! /athena/ihlab/scratch/bes4014/mambaforge-pypy3/bin/GraphAligner -g /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa -f /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly.fasta -a /athena/ihlab/scratch/bes4014/contigs.gaf -x dbg
python edges.py /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa /athena/ihlab/scratch/bes4014/masked_reads.gaf /athena/ihlab/scratch/bes4014/masked_contig.gaf /athena/ihlab/scratch/bes4014
./prune_graph_edges.sh /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa /athena/ihlab/scratch/bes4014/edges.csv
python pruned_fasta.py /athena/ihlab/scratch/bes4014/edges.gfa /athena/ihlab/scratch/bes4014
./minimap2-2.24_x64-linux/minimap2 -a /athena/ihlab/scratch/bes4014/edges_pruned.fasta /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/GCA_000020605.1_ASM2060v1_genes.fna > /athena/ihlab/scratch/bes4014/reads.sam
python gene.py /athena/ihlab/scratch/bes4014/reads.sam /athena/ihlab/scratch/bes4014

conda deactivate

exit
