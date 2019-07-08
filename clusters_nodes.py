import csv, json, sys

## INPUT
LABELS = json.load(open('example/labels')) # devrait être juste une liste de label mais bon
EDGES = open("example/X.sp_mat").read() # sparse X

## OUTPUT
TO_BE_DISPLAYED = sys.argv[1] # ex: 7Ccluster(5,5,2)
CLUSTERS = open("example/out/" + TO_BE_DISPLAYED).read()



clusters = [int(x) for x in 
    list(csv.reader([CLUSTERS], delimiter=' '))[0]
    if x is not '']

clusters_nodes = {}

"""
labels = list(csv.reader([LABELS], delimiter=' '))[0]

def get_label(node):
	if len(labels) > node:
		return labels[node]
	return "no-label-%s" % node
"""
labels = LABELS
def get_label(node):
	return labels.get(str(node), "no-label-%s" % node)


def add_one(node):
    cluster = clusters[node]
    if cluster not in clusters_nodes:
        clusters_nodes[cluster] = {}
    clust_nodes = clusters_nodes[cluster]
    if node not in clust_nodes:
        clust_nodes[node] = 0
    clust_nodes[node] += 1

for line in csv.reader(EDGES.split('\n'), delimiter=' '):
    if len(line) == 3:
        source, target, val = line
        if val == '0':
            continue
        add_one(int(source))
        add_one(int(target))

def top_10(cluster):
    nodes = clusters_nodes.get(cluster, {})
    return [get_label(node) for node, _ in
                sorted(nodes.items(), key=lambda it: -it[1]) #[:10]
            ]

top_nodes = [top_10(cluster) for cluster in range(max(clusters) + 1)]
# return top_nodes # [ [label1_for_cluster_1, label2], [label4_for_cluster_2, label3],.. ]

for i, cluster in enumerate(top_nodes):
	print("> cluster", i)
	for node in cluster:
		print(' -- ', node)
