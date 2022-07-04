#! /bin/bash -l

#SBATCH --partition=panda
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=pipeline

conda activate

#! /athena/ihlab/scratch/bes4014/mambaforge-pypy3/bin/GraphAligner -g /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa -f /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis.fastq -a /athena/ihlab/scratch/bes4014/test/reads.gaf -x dbg
/athena/ihlab/scratch/bes4014/mambaforge-pypy3/bin/GraphAligner -g /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa -f /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly.fasta -a /athena/ihlab/scratch/bes4014/test/contigs.gaf -x dbg
python edges.py /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa /athena/ihlab/scratch/bes4014/test/reads.gaf /athena/ihlab/scratch/bes4014/test/contigs.gaf /athena/ihlab/scratch/bes4014/test
./prune_graph_edges.sh /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa /athena/ihlab/scratch/bes4014/test/edges.csv
python pruned_fasta.py /athena/ihlab/scratch/bes4014/test/edges.gfa /athena/ihlab/scratch/bes4014/test
./minimap2-2.24_x64-linux/minimap2 -a /athena/ihlab/scratch/bes4014/test/edges_pruned.fasta /athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/GCA_000020605.1_ASM2060v1_genes.fna > /athena/ihlab/scratch/bes4014/test/reads.sam
python gene.py /athena/ihlab/scratch/bes4014/test/reads.sam /athena/ihlab/scratch/bes4014/test

conda deactivate

exit
