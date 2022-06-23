import numpy as np
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
with open("/athena/ihlab/scratch/bes4014/ex_612_gene.sam", "r") as infile:
  reads = {}
  lines = infile.readlines()
  for line in lines:
    l = line.split()
    if l[0][0] != "@":
      if l[2] != "*":
        if l[2] in reads:
          reads[l[2]] += 1
        else:
          reads[l[2]] = 1
data = np.array(list(reads.values()))
percentile = np.percentile(data, 95,interpolation='linear')
readprint = []
for key in reads:
  if reads[key] >= percentile:
    readprint.append(key)

sequences = []
with open("/athena/ihlab/scratch/bes4014/ex_612.fasta", "r") as reads_f:
  for record in SeqIO.parse(reads_f, "fasta"):
    if record.id in readprint:
      sequences.append(record)

with open("/athena/ihlab/scratch/bes4014/ex_567_gene.sam", "r") as infile:
  reads = {}
  lines = infile.readlines()
  for line in lines:
    l = line.split()
    if l[0][0] != "@":
      if l[2] != "*":
        if l[2] in reads:
          reads[l[2]] += 1
        else:
          reads[l[2]] = 1

data = np.array(list(reads.values()))
percentile = np.percentile(data, 95,interpolation='linear')
readprint = []
for key in reads:
  if reads[key] >= percentile:
    readprint.append(key)

with open("/athena/ihlab/scratch/bes4014/ex_567.fasta", "r") as reads_f:
  for record in SeqIO.parse(reads_f, "fasta"):
    if record.id in readprint:
      sequences.append(record)

with open("/athena/ihlab/scratch/bes4014/ex_filt.fasta", "w") as outfile:
  SeqIO.write(sequences, outfile, "fasta")

with open("/athena/ihlab/scratch/bes4014/commonreads_gene.sam", "r") as infile:
  reads = {}
  lines = infile.readlines()
  for line in lines:
    l = line.split()
    if l[0][0] != "@":
      if l[2] != "*":
        if l[2] in reads:
          reads[l[2]] += 1
        else:
          reads[l[2]] = 1

data = np.array(list(reads.values()))
percentile = np.percentile(data, 95,interpolation='linear')
print(percentile)
readprint = []
for key in reads:
  if reads[key] >= percentile:
    readprint.append(key)

sequences = []
with open("/athena/ihlab/scratch/bes4014/commonreads.fasta", "r") as reads_f:
  for record in SeqIO.parse(reads_f, "fasta"):
    if record.id in readprint:
      sequences.append(record)
with open("/athena/ihlab/scratch/bes4014/commonreads_filt.fasta", "w") as outfile:
  SeqIO.write(sequences, outfile, "fasta")
