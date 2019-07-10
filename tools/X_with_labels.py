import csv, json

X = open("example/X.sp_mat").read() # sparse X
Clabels = json.load(open("example/Clabels"))
Rlabels = json.load(open("example/Rlabels"))

n_cols = 0
n_rows = 0

coords = []
rows = set()
cols = set()
for line in csv.reader(X.split('\n'), delimiter=' '):
    if line:
        r, c, val = [int(float(x)) for x in line]
        print(r, c, Rlabels[str(r)], Clabels[str(c)])