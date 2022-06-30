import sys
import csv
import re
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
csv.field_size_limit(sys.maxsize)

graphs = []
paths = []
f_link = open("/athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph_pruned_10_2700.gfa","r")
lines = f_link.readlines()
for line in lines:
  l = line.split()
  if(l[0] == "L"):
    graphs.append(set((l[1],l[3])))
  if(l[0] == "P"):
    paths.append(l[2].split(","))

merged = True
while merged:
  merged = False
  results = []
  while graphs:
    common, rest = graphs[0], graphs[1:]
    graphs = []
    for x in rest:
      if x.isdisjoint(common):
        graphs.append(x)
      else:
        merged = True
        common |= x
    results.append(common)
  graphs = results

with open("/athena/ihlab/scratch/bes4014/link.csv", "w") as outfile:
  writer = csv.writer(outfile)
  for graph in graphs:
    writer.writerow(graph)

with open("/athena/ihlab/scratch/bes4014/edges.csv", "r") as infile:
  reader = csv.reader(infile, delimiter=';')
  for row in reader:
    if row[0]==str(567):
      text=row[4].replace('[','{').replace(']','}')
      r_567=eval(text)
    if row[0]==str(612):
      text=row[4].replace('[','{').replace(']','}')
      r_612=eval(text)

r_567_612 = r_567.intersection(r_612)

r_567_ex = r_567.difference(r_612)
r_612_ex = r_612.difference(r_567)

sequences_ex_567 = []
sequences_ex_612 = []
sequences = []
with open("/athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis.fastq", "r") as reads_f:
  for record in SeqIO.parse(reads_f, "fastq"):
    if record.id in r_567_612:
      sequences.append(record)
    if record.id in r_567_ex:
      sequences_ex_567.append(record)
    if record.id in r_612_ex:
      sequences_ex_612.append(record)

with open("/athena/ihlab/scratch/bes4014/commonreads.fasta", "w") as outfile:
  SeqIO.write(sequences, outfile, "fasta")

with open("/athena/ihlab/scratch/bes4014/ex_567.fasta", "w") as outfile:
  SeqIO.write(sequences_ex_567, outfile, "fasta")

with open("/athena/ihlab/scratch/bes4014/ex_612.fasta", "w") as outfile:
  SeqIO.write(sequences_ex_612, outfile, "fasta")

print(sequences_ex_567)
print(sequences_ex_612)
