import csv

TDM = open("example/TDM.sp_mat").read() # sparse X

n_cols = 0
n_rows = 0

coords = []
rows = set()
cols = set()
for line in csv.reader(TDM.split('\n'), delimiter=' '):
    if line:
        r, c, val = [int(float(x)) for x in line]
        coords.append([r, c, val])
        n_cols = max(c, n_cols)
        n_rows = max(r, n_rows)
        rows.add(r)
        cols.add(c)

print('detected size:', n_rows, 'rows,', n_cols, 'cols')
for r in range(n_rows):
    if r not in rows:
        print('empty row', r)
for c in range(n_cols):
    if c not in cols:
        print('empty col', c)