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

  def __init__ (self, id, length, sequence):
    self.id = id
    self.length = length
    self.sequence = sequence
    self.reads = []
  
  def __iter__(self):
    return iter([self.id, self.length, self.coverage_reads, self.sequence, self.reads])

  def addReads(self, read):
    self.reads.append(read)

f_gr = open("/athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa","r")
lines = f_gr.readlines()
edges = {}
for index, line in enumerate(lines):
  l = line.split()
  if(l[0] == "S"):
    edges[index] = Edge(index, len(l[2]), l[2])

f_al = open("/athena/ihlab/scratch/bes4014/masked_reads.gaf","r")
f_readsperc = open("/athena/ihlab/scratch/bes4014/reads_perc.txt","w")
lines = f_al.readlines()
count_coverage = np.zeros(len(edges))
for line in lines: #for every reads
  l = line.split()
  e = re.split("<|>",l[5]) #edge mapped to the reads
  for ed in e:
    if ed != "":
      x = int(ed[5:])
      count_coverage[x-1] += int(l[9])
      reads_perc = (int(l[3])-int(l[2]))/int(l[1])
      if reads_perc >=0.75:
        edges[x].addReads(l[0])
      else:
        f_readsperc.write(str(x)+","+l[0]+","+str(reads_perc)+"\n")

for index, e in edges.items():
  e.coverage_reads = count_coverage[index-1]/e.length

sequences = []
fieldnames = ['id', 'length', 'coverage_reads', 'sequence', 'reads']
low_cov = open("/athena/ihlab/scratch/bes4014/low_cov.csv", "w")
low_len = open("/athena/ihlab/scratch/bes4014/low_len.csv", "w")
with open("/athena/ihlab/scratch/bes4014/edges.csv", "w") as outfile:
  writer = csv.writer(outfile,delimiter=';')
  writer.writerow(fieldnames)
  for index in list(edges):
    if(edges[index].coverage_reads>=10 and edges[index].length>=2700):
      writer.writerow(edges[index])
      sequence = SeqRecord(Seq(edges[index].sequence),"edge_"+str(index),"","")
      sequences.append(sequence)
    else:
      if(edges[index].coverage_reads<10):
        csv.writer(low_cov).writerow(edges[index])
      else:
        csv.writer(low_len).writerow(edges[index])
      edges.pop(index)

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
with open("/athena/ihlab/scratch/bes4014/edges.fasta", "w") as output_handle:
  SeqIO.write(sequences, output_handle, "fasta")

edgestowrite = []
for sequence in sequences:
  if sequence.id == "edge_567" or sequence.id == "edge_612":
    edgestowrite.append(sequence)

with open("/athena/ihlab/scratch/bes4014/edges_567_612.fasta", "w") as output_handle:
  SeqIO.write(edgestowrite, output_handle, "fasta")
