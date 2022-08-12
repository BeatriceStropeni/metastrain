import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description="")
parser.add_argument("sam_path", type=str, help="SAM file path")
parser.add_argument("save_path", type=str, help="Path for storing file, don't insert / at the end")
args = parser.parse_args()

edges = {}
with open(args.sam_path, "r") as infile:
  lines = infile.readlines()
  for line in lines:
    l = line.split()
    if l[0][0] != "@":
      if l[2] != "*":
        if l[2] in edges:
          for idx, tup in enumerate(edges[l[2]]):
            if int(l[3])<tup[1]:
              edges[l[2]].insert(idx,(l[0],int(l[3])))
              break
            else:
              if idx == len(edges[l[2]])-1:
                edges[l[2]].insert(idx+1,(l[0],int(l[3])))
                break
        else:
          edges[l[2]] = [(l[0],int(l[3]))]

with open(args.save_path+"/"+Path(args.sam_path).stem+"_gene.csv", "w") as outfile:
  for idx, edge in edges.items():
    for tup in edge:
      outfile.write(idx+"\t"+tup[0]+"\t"+str(tup[1])+"\n")

