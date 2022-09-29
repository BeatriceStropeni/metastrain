import csv
import sys
import math
from decimal import *
csv.field_size_limit(sys.maxsize)
  
def get_interval(test_list):
  res = []
  temp = []
  is_up = True
  if test_list[0] > test_list[1]:
      is_up = False

  for curr, nex in zip(test_list, test_list[1:]):
    temp.append(curr)

    if (nex > curr and not is_up) or (nex< curr and is_up) or (abs(nex-curr)>1 ):
      if len(temp)>1:
        x = [int(temp[0]),int(temp[-1])]
        temp = x
      res.append(temp)
      temp = []
      is_up = not is_up
       
  temp.append(nex)
  if len(temp)>1:
      x = [int(temp[0]),int(temp[-1])]
      temp = x 
  res.append(temp)

  return res

parser = argparse.ArgumentParser(description="")
parser.add_argument("gfa_path", type=str, help="GFA file path")
parser.add_argument("csv_path_edges", type=str, help="CSV file path for edges info")
parser.add_argument("csv_path_gene_edges", type=str, help="CSV file path for gene annotation")
parser.add_argument("save_path", type=str, help="Path for storing file, don't insert / at the end")
args = parser.parse_args()

#find conflicts
links = {}
with open(args.gfa_path, "r") as input:
  lines = input.readlines()
  for line in lines:
    l = line.split()
    if(l[0] == "L"):
      rc = l[6].split(":")[2]
      if l[1] in links:
        links[l[1]].append([l[2],(l[3],rc),l[4]])
      else:
        links[l[1]]=[[l[2],(l[3],rc),l[4]]]

genes = {}
with open(args.csv_path_gene_edges, "r") as input:
  lines = input.readlines()
  for line in lines:
    l = line.split()
    gene_num = int(l[1].split("_")[-1])
    if l[0] in genes:
      genes[l[0]].append(int(gene_num))
    else:
      genes[l[0]] = [int(gene_num)]

for gene in genes:
  if len(genes[gene])>1:
    genes[gene] = get_interval(genes[gene])

edges = {}
with open(args.csv_path_edges, "r") as input:
  reader = csv.reader(input, delimiter=';')
  for row in reader:
    if row[0] != "id":
      edges["edge_"+row[0]] = [row[1],round(Decimal(row[3]),2)]

with open(args.save_path+"/linkoverview.csv", "w") as outfile:
  outfile.write("start node \tlength \tcoverage \tgene \tlink direction \tfinish node \tlength \tcoverage \tgene \tlink direction \tread count link\n")
  for idx, link in links.items():
    for elem in link:
      printstr = idx+"\t"+edges[idx][0]+"\t"+str(edges[idx][1]).replace(".",",")+"\t"
      if idx in genes:
        printstr+=str(genes[idx])+"\t"
      else:
        printstr+="0\t"
      printstr+=elem[0]+"\t"+elem[1][0]+"\t"+edges[elem[1][0]][0]+"\t"+str(edges[elem[1][0]][1]).replace(".",",")+"\t"
      if elem[1][0] in genes:
        printstr+=str(genes[elem[1][0]])+"\t"
      else:
        printstr+="0\t"
      printstr+=elem[2]+"\t"+elem[1][1]+"\n"
      outfile.write(printstr)
