from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("gfa_path", type=str, help="GFA file path")
parser.add_argument("save_path", type=str, help="Path for storing file, don't insert / at the end")
args = parser.parse_args()

sequences = []
f_gr = open(args.gfa_path,"r")
lines = f_gr.readlines()
edges = {}
for line in lines:
  l = line.split()
  if(l[0] == "S"):
    sequence = SeqRecord(Seq(l[2]),l[1],"","")
    sequences.append(sequence)

with open(args.save_path+"/edges_pruned.fasta", "w") as output_handle:
  SeqIO.write(sequences, output_handle, "fasta")
