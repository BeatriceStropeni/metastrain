import csv

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
