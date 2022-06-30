import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description="")
parser.add_argument("sam_path", type=str, help="SAM file path")
parser.add_argument("save_path", type=str, help="Path for storing file, don't insert / at the end")
args = parser.parse_args()

f_sam = open(args.sam_path,"r")
lines = f_sam.readlines()
reads = {}
for line in lines:
  l = line.split()
  if(l[0][0] != "@"):
    if(l[0] in reads):
      reads[l[0]].append(l[2])
    else:
      reads[l[0]] = [l[2]]
with open(args.save_path+"/"+Path(args.sam_path).stem+"_gene.csv", "w") as outfile:
  outfile.write('element genes \n')
  for index, e in reads.items():
    outfile.write(index+','+str(e)+'\n')
f_sam.close()
