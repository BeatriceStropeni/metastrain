import argparse
import numpy as np
import re
import csv
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

class Edge:
  id = 0
  length = 0
  sequence = ""
  coverage_reads = 0
  reads = None
  coverage_contigs = 0
  contigs = None

  def __init__ (self, id, length, sequence):
    self.id = id
    self.length = length
    self.sequence = sequence
    self.reads = []
    self.contigs = []

  def __iter__(self):
    return iter([self.id, self.length, self.contigs, self.reads, self.coverage_reads, self.coverage_contigs])

  def addReads(self, read):
    self.reads.append(read)

  def addContigs(self, contig):
    self.contigs.append(contig)

parser = argparse.ArgumentParser(description="")
parser.add_argument("gfa_path", type=str, help="GFA file path")
parser.add_argument("gaf_path_reads", type=str, help="GAF file path for the reads alignment")
parser.add_argument("gaf_path_contigs", type=str, help="GAF file path for the contigs alignment")
parser.add_argument("save_path", type=str, help="Path for storing file, don't insert / at the end")
args = parser.parse_args()

f_gr = open(args.gfa_path,"r")
lines = f_gr.readlines()
edges = {}
for index, line in enumerate(lines):
  l = line.split()
  if(l[0] == "S"):
    edges[index] = Edge(index, len(l[2]), l[2])

f_al = open(args.gaf_path_reads,"r")
lines = f_al.readlines()
count_coverage = np.zeros(len(edges))
for line in lines: #for every reads
  l = line.split()
  e = re.split("<|>",l[5]) #edge mapped to the reads
  for ed in e:
    if ed != "":
      x = int(ed[5:])
      reads_perc = (int(l[3])-int(l[2]))/int(l[1])
      if reads_perc >=0.75:
        edges[x].addReads(l[0])
        count_coverage[x-1] += int(l[9])

for index, e in edges.items():
  e.coverage_reads = count_coverage[index-1]/e.length

f_al = open(args.gaf_path_contigs,"r")
lines = f_al.readlines()
count_coverage = np.zeros(len(edges))
for line in lines: #for every reads
  l = line.split()
  e = re.split("<|>",l[5]) #edge mapped to the reads
  for ed in e:
    if ed != "":
      x = int(ed[5:])
      count_coverage[x-1] += int(l[9])
      edges[x].addContigs(l[0])

for index, e in edges.items():
  e.coverage_contigs = count_coverage[index-1]/e.length

sequences = []
fieldnames = ['id', 'length', 'contigs', 'reads', 'coverage_reads', 'coverage_contigs']
with open(args.save_path+"/edges.csv", "w") as outfile:
  writer = csv.writer(outfile,delimiter=';')
  writer.writerow(fieldnames)
  for index in list(edges):
    if(edges[index].coverage_reads>=10):
      writer.writerow(edges[index])
      sequence = SeqRecord(Seq(edges[index].sequence),"edge_"+str(index),"","")
      sequences.append(sequence)
    else:
      edges.pop(index)

with open(args.save_path+"/edges.fasta", "w") as output_handle:
  SeqIO.write(sequences, output_handle, "fasta")
