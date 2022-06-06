import sys
import matplotlib.pyplot as plt

filename = sys.argv[1]
grid_dimension = int(sys.argv[2])
max_value = int(sys.argv[3])

mat = [[0 for _ in range(grid_dimension)] for _ in range(grid_dimension)]


V = {}
IV = {}

for i in range(grid_dimension):
	for j in range(grid_dimension):
		for k in range(1, max_value+1):
			V[(i, j, k)] = len(V) + 1
			IV[V[(i, j, k )]] = (i, j, k)

def pprint(M):
	def extend(a):
		out = []
		for sublist in a:
			out.extend(sublist)
		return out
	flat = extend(M)
	print(", ".join(map(str, flat)))
	# for row in M:
	# 	print(" ".join(map(str, row)))

def visualize(M, text=True):
	fig, ax = plt.subplots()
	im = ax.imshow(M, cmap="tab20b")
	if text:
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

def visualize_decomposition(M, text=False):
	colors = {}
	for row in M:
		for elem in row:
			colors[elem] = 1
	for color in colors:
		visualize_color(M, color, text)
	

def visualize_color(M, color, text=False):
	fig, ax = plt.subplots()
	M_copy = [[0 for col in M[0]] for row in M]
	for i in range(len(M)):
		for j in range(len(M[0])):
			if M[i][j] == color:
				M_copy[i][j] = color 
	im = ax.imshow(M_copy, cmap="tab20b")
	if text:
		for i in range(len(M)):
			for j in range(len(M[0])):
				if M[i][j] == color:
					text = ax.text(j, i, M[i][j],
								ha="center", va="center", color="w")
	ax.set_title(f"Solution to a {len(M)}x{len(M[0])} grid highlighting color {color} ")
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
			if v in IV and len(IV[v]) == 3:
				i, j, value = IV[v]	
				mat[i][j] = value
	assert (valid(mat))
	pprint(mat)
	visualize(mat, text=False)
	visualize_decomposition(mat, text=False)

