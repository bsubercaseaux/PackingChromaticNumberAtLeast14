import sys
import matplotlib.pyplot as plt

filename = sys.argv[1]
radius = int(sys.argv[2])
colors = int(sys.argv[3])

V = {}
IV = {}

for i in range(-radius, radius+1):
	for j in range(-radius, radius+1):
		if abs(i) + abs(j) > radius: continue
		for color in range(1, colors+1):
			V[(i,j,color)] = len(V) + 1
			IV[V[(i,j,color)]] = (i,j,color)
for r in range(1, radius+1):
	V[r] = len(V) + 1
	IV[V[r]] = r

def mat_from_coloring(coloring):
	mat = [[0 for _ in range(2*radius+1)] for _ in range(2*radius+1)]
	for key, val in coloring.items():
		i,j = key
		mat[i+radius][j+radius] = val
	return mat

def print_mat(mat):
	for row in mat:
		print(", ".join(list(map(str, row))))

def visualize(M, text=True):
	fig, ax = plt.subplots()
	im = ax.imshow(M, cmap="tab20b")
	if text:
		for i in range(len(M)):
			for j in range(len(M[0])):
				if M[i][j] != 0:
					text = ax.text(j, i, M[i][j],
								ha="center", va="center", color="w")
	colors = {}
	for row in M:
		for elem in row:
			colors[elem] = 1
	ax.set_title(f"Solution to a {(len(M)-1)//2} diamond using {len(colors.keys())-1} colors")
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
	ax.set_title(f"Solution to a {(len(M)-1)//2} diamond highlighting color {color} ")
	plt.show()

with open(filename, 'r') as file:
	L = []
	for line in file:
		s = line.replace('\n', '').split(' ')
		first_int = 0
		while True:
			try:
				i = int(s[first_int])
				break
			except:
				first_int += 1
		try:
			L.extend(list(map(int, s[first_int:])))
		except:
			print(s)
			exit(0)

	coloring = {}
	print(L)
	for v in L:
		if v > 0 and v in IV:
			try:
				print("v is positive")
				i, j, color = IV[v]
				coloring[(i,j)] = color
			except:
				continue
	mat = mat_from_coloring(coloring)
	print_mat(mat)
	visualize(mat, text=True)
	visualize_decomposition(mat)
	

