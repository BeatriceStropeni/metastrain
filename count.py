from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

kmer = {}
k = 15
with open("/athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis.fastq", "r") as reads_f:
  for record in SeqIO.parse(reads_f, "fasta"):
    i = 0
    while i+k<len(record.seq):
      if record.seq[i:i+k] in kmer:
        kmer[record.seq[i:i+k]] +=1
      else:
        kmer[record.seq[i:i+k]] =1
      i+=1
print(kmer)
