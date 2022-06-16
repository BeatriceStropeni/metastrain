link = []
paths = []
f_gr = open("/athena/masonlab/scratch/users/lam4003/MIAB_Nanopore_99/sample_6_mag_20/agathobacter_rectalis/assembly_graph.gfa","r")
lines = f_gr.readlines()
for line in lines:
  l = line.split()
  if(l[0] == "L"):
    startedge = l[1].split("_")[1]
    endedge = l[3].split("_")[1]
    if startedge == "567" or startedge == "612" or endedge == "567" or endedge == "612":
      link.append([l[1],l[3]])
  if l[0] == "P":
    edges = l[2].split(",")
    for edge in edges:
      edge_n = edge[0:-1].split("_")[1]
      if edge_n == "612" or edge_n == "567":
        paths.append(l[2])
print(link)
print(paths)

