import numpy as np
import csv
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

class Edge:
  id = 0
  length = 0
  sequence = ""

  def __init__ (self, id, length, sequence):
    self.id = id
    self.length = length
    self.sequence = sequence

  def __iter__(self):
    return iter([self.id, self.length, self.sequence])

f_gr = open("/athena/ihlab/scratch/bes4014/ex_filt/assembly_graph.gfa","r")
lines = f_gr.readlines()
edges = {}
for index, line in enumerate(lines):
  l = line.split()
  if(l[0] == "S"):
    edges[index] = Edge(index, len(l[2]), l[2])

sequences = []
fieldnames = ['id', 'length', 'sequence']
with open("/athena/ihlab/scratch/bes4014/csv/ex_edges.csv", "w") as outfile:
  writer = csv.writer(outfile,delimiter=';')
  writer.writerow(fieldnames)
  for index in list(edges):
    writer.writerow(edges[index])
    sequence = SeqRecord(Seq(edges[index].sequence),"edge_"+str(index),"","")
    sequences.append(sequence)

with open("/athena/ihlab/scratch/bes4014/fasta/ex_edges.fasta", "w") as output_handle:
  SeqIO.write(sequences, output_handle, "fasta")
