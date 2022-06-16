import sys
import csv
import re
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
csv.field_size_limit(sys.maxsize)
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

r_567_filtered = set()
r_612_filtered = set()
with open("/athena/ihlab/scratch/bes4014/masked_reads.gaf", "r") as gaffile:
  lines = gaffile.readlines()
  for line in lines:
    l = line.split()
    if l[0] in r_567_612:
      e = re.split("<|>",l[5])
      for ed in e:
        if ed[5:] == "567" and int(l[8])<20000:
          r_567_filtered.add(l[0])
        if ed[5:] == "612" and int(l[7])>107243:
          r_612_filtered.add(l[0])

filtered_inters=r_567_filtered.intersection(r_612_filtered)

writelines= []
with open("/athena/ihlab/scratch/bes4014/masked_reads.gaf", "r") as gaffile:
  lines = gaffile.readlines()
  for line in lines:
    l = line.split()
    if l[0] in filtered_inters:
      e = re.split("<|>",l[5])
      if e[1][5:] == "567" or e[1][5:] == "612":
        writelines.append(line) 

with open("/athena/ihlab/scratch/bes4014/dataedgefiltering.csv", "w") as outfile:
  for line in writelines:
    outfile.write(line)

sequences = []
with open("/athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis.fastq", "r") as reads_f:
  for record in SeqIO.parse(reads_f, "fastq"):
    if record.id in r_567_612:
      sequences.append(record)

with open("/athena/ihlab/scratch/bes4014/commonreads.fasta", "w") as outfile:
  SeqIO.write(sequences, outfile, "fasta")

commonedges = []
with open("/athena/ihlab/scratch/bes4014/edges.csv", "r") as infile:
  reader = csv.reader(infile, delimiter=';')
  for row in reader:
    if row[0] != "id":
      text=row[4].replace('[','{').replace(']','}')
      readslist = None
      readslist=eval(text)
      if r_567_612.isdisjoint(readslist):
        commonedges.append("edges_"+row[0])

print(commonedges)
print(len(commonedges))
