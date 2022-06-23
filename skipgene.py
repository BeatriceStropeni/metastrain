from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

with open("/athena/ihlab/scratch/bes4014/edges_567_612.sam", "r") as gene_ann_f:
  lines = gene_ann_f.readlines()
  for line in lines:
    l = line.split()
    if l[0] == "lcl|CP001107.1_gene_1592":
      start = l[3]
      length = len(l[9])
      print(line)

with open("/athena/ihlab/scratch/bes4014/edges_567_612.fasta", "r") as reads_f:
  for record in SeqIO.parse(reads_f, "fasta"):
    if record.id == "edge_567":
      print("A")
