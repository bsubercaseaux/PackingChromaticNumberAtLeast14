import sys

filename = sys.argv[1]
n_nodes = int(sys.argv[2])
colors = int(sys.argv[3])

V = {}
IV = {}

for i in range(n_nodes):
	for color in range(1, colors+1):
		V[f"X_{i,color}"] = len(V) + 1
		IV[V[f"X_{i,color}"]] = f"X_{i,color}"


with open(filename, 'r') as file:
	L = []
	for line in file:
		s = line.replace('\n', '').split(' ')
		L.extend(list(map(int, s[1:])))

	coloring = {}
	for v in L:
		if v > 0:
			print(f"v={v}, variable {IV[v]} is true")
			i, color = IV[v][3:-1].split(", ")
			coloring[i] = color
	for key, val in coloring.items():
		print(f"node {key} receives color {val}")
	#pprint(mat)
	

