f_sam = open("/athena/ihlab/scratch/bes4014/contig.sam","r")
lines = f_sam.readlines()
reads = {}
for line in lines:
  l = line.split()
  if(l[0][0] != "@"):
    if(l[0] in reads):
      reads[l[0]].append(l[2])
    else:
      reads[l[0]] = [l[2]]
with open("/athena/ihlab/scratch/bes4014/gene_contig.csv", "w") as outfile:
  outfile.write('contig, genes \n')
  for index, e in reads.items():
    outfile.write(index+','+str(e)+'\n')
f_sam.close()

f_sam = open("/athena/ihlab/scratch/bes4014/reads.sam","r")
lines = f_sam.readlines()
reads = {}
for line in lines:
  l = line.split()
  if(l[0][0] != "@"):
    if(l[0] in reads):
      reads[l[0]].append(l[2])
    else:
      reads[l[0]] = [l[2]]
with open("/athena/ihlab/scratch/bes4014/gene_reads.csv", "w") as outfile:
  outfile.write('read, genes \n')
  for index, e in reads.items():
    outfile.write(index+','+str(e)+'\n')
f_sam.close()

f_sam = open("/athena/ihlab/scratch/bes4014/edges.sam","r")
lines = f_sam.readlines()
reads = {}
for line in lines:
  l = line.split()
  if(l[0][0] != "@"):
    if(l[0] in reads):
      reads[l[0]].append(l[2])
    else:
      reads[l[0]] = [l[2]]
with open("/athena/ihlab/scratch/bes4014/gene_edges.csv", "w") as outfile:
  outfile.write('edge, genes \n')
  for index, e in reads.items():
    outfile.write(index+','+str(e)+'\n')
f_sam.close()
