from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

records = []
with open("/athena/ihlab/scratch/bes4014/edges_567_612.fasta", "r") as reads_f:
  for record in SeqIO.parse(reads_f, "fasta"):
    if record.id == "edge_567":
      records.append(SeqRecord(record.seq.reverse_complement(),record.id,"",""))
    else:
      records.append(record)

with open("/athena/ihlab/scratch/bes4014/edges_567rc_612.fasta", "w") as outfile:
  SeqIO.write(records, outfile, "fasta")
