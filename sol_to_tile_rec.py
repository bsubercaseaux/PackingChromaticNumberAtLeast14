import sys
import matplotlib.pyplot as plt
import math

filename = sys.argv[1]
grid_dimension = int(sys.argv[2])
max_value = int(sys.argv[3])

V = {}
IV = {}

powers_of_two = [2**k for k in range(math.ceil(math.log2(max_value)))]

for i in range(grid_dimension):
	for j in range(grid_dimension):
		for v in range(1, max_value+1):
			V[f"X_{i,j,v}"] = len(V) + 1
			IV[V[f"X_{i,j,v}"]] = f"X_{i,j,v}"

# Important: all X variables need to be created before the P variables!
for i in range(-max_value+1, grid_dimension + max_value):
	for j in range(-max_value+1, grid_dimension + max_value):
		for v in range(1, max_value+1):
			for k, pw in enumerate(powers_of_two):
				if pw > v: break
				V[f"P_{i, j, v, pw}"] = len(V) + 1
				IV[V[f"P_{i,j,v,pw}"]] = f"P_{i,j,v,pw}"

mat = [[0 for _ in range(grid_dimension)] for _ in range(grid_dimension)]

def pprint(M):
	for row in M:
		print(" ".join(map(str, row)))

def visualize(M):
	fig, ax = plt.subplots()
	im = ax.imshow(M, cmap="tab20b")
	for i in range(len(M)):
		for j in range(len(M[0])):
			text = ax.text(j, i, M[i][j],
						ha="center", va="center", color="w")
	colors = {}
	for row in M:
		for elem in row:
			colors[elem] = 1
	ax.set_title(f"Solution to a {len(M)}x{len(M[0])} grid using {len(colors.keys())} colors")
	plt.show()

def valid(M):
	for i in range(len(M)):
		for j in range(len(M[0])):
			for a in range(i, len(M)):
				for b in range(len(M[0])):
					if i == a and j == b:
						continue
					if M[i][j] == M[a][b] and (a-i + abs(b-j) <= M[i][j]):
						print(f"Conflict for number {M[i][j]}, at positions ({i}, {j}) and ({a}, {b})")
						return False
	return True

with open(filename, 'r') as file:
	L = []
	for line in file:
		s = line.replace('\n', '').split(' ')
		L.extend(list(map(int, s[1:])))

	for v in L:
		if v > 0:
			if "X" in IV[v]:
				i, j, val = IV[v][3:-1].split(", ")
				mat[int(i)][int(j)] = int(val) 
	pprint(mat)
	assert (valid(mat))
	# visualize(mat)

