import sys
import csv
import re
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
csv.field_size_limit(sys.maxsize)

edges=[]
with open("/athena/ihlab/scratch/bes4014/ex_filt/edges.csv", "r") as infile:
  reader = csv.reader(infile, delimiter=';')
  for row in reader:
    if row[3] != "reads":
      text=row[3].replace('[','{').replace(']','}')
      edges.append(eval(text))

print(len(edges[4].intersection(edges[5])))
print(len(edges[4].intersection(edges[6])))
print(len(edges[5].intersection(edges[6])))
