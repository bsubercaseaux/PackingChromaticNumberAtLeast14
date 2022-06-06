import sys


V = {}

def clause_to_text(clause):
	return " ".join(map(str, clause + [0]))

def write_to_file(clauses, vars, filename):
	with open(filename, 'w') as file:
		file.write(f"p cnf {vars} {len(clauses)}\n")
		for clause in clauses:
			file.write(clause_to_text(clause) + '\n')

def vdirs_k(k):
		vdirs = []
		for i in range(k+1):
			for j in range(k+1-i):
				if i + j == 0: continue # distance > 0
				_is = set([i, -i])
				_js = set([j, -j])
				for _i in _is:
					for _j in _js:
						vdirs.append((_i, _j))
		return vdirs

def split(arr, parts):
	ans = []
	arr = list(arr)
	l = (len(arr)+parts-1)//parts
	for p in range(parts):
		ans.append(arr[l*p: min(l*(p+1), len(arr))])
	return ans
assert split(range(1,11), 3) == [[1,2,3,4],[5,6,7,8],[9, 10]]

def generate(filename, grid_dimension, max_value, wrap=True, checkerboard=True, central_force=True):
	clauses = []
	## clauses for each position having at least a color!
	commander = False # unused
	n_commander = 4
	color_split = split(range(1, max_value+1), n_commander)
	

	for i in range(grid_dimension):
		for j in range(grid_dimension):
			for k in range(1, max_value+1):
				V[(i,j,k)] = len(V) + 1
	if commander:
		for i in range(grid_dimension):
			for j in range(grid_dimension):
				c_clauses = [[] for _ in range(n_commander)]
				for c in range(n_commander):
					V[(c, (i,j))] = len(V) + 1
					c_clauses[c].append(-V[(c, (i,j))])
					for color in color_split[c]:
						c_clauses[c].append(V[(i,j, color)])
				clauses.extend(c_clauses)
				clauses.append([V[(c, (i,j))] for c in range(n_commander)])
	else:
		for i in range(grid_dimension):
			for j in range(grid_dimension):
				clauses.append([V[(i,j, color)] for color in range(1, max_value+1)])
					

	# force checkerboard of ones
	if checkerboard:
		print("checkerboard of ones forced")
		for i in range(grid_dimension):
				for j in range(grid_dimension):
					if (i+j)%2 == grid_dimension%2:
						clauses.append([V[(i,j,1)]])
	if central_force:
		clauses.append([V[(grid_dimension//2, grid_dimension//2, min(max_value, grid_dimension//2))]])

	## clauses forbidding x_{i,j,v} and x_{a,b,v} if dist(i, j, a, b) <= v.
	for number in range(1, max_value+1): 
		vdirs = vdirs_k(number)
		for i in range(grid_dimension):
			for j in range(grid_dimension):
				for vdir in vdirs:
					di, dj = vdir
					if wrap:
						new_i, new_j = (i+grid_dimension+di)%grid_dimension, (j+grid_dimension+dj)%grid_dimension
						if new_i == i and new_j == j: continue
					else:
						new_i, new_j = i+di, j +dj
						if new_i < 0 or new_i >= grid_dimension or new_j < 0 or new_j >= grid_dimension:
							continue	
					clauses.append([-V[(i, j, number)], -V[(new_i, new_j, number)]])
	write_to_file(clauses, len(V), filename)
	print(f"# variables = {len(V)}, # clauses = {len(clauses)}")

if len(sys.argv) > 5:
	
	filename = sys.argv[1]

	grid_dimension = int(sys.argv[2])
	max_value = int(sys.argv[3])
	

	wrap = bool(int(sys.argv[4]))
	checkerboard = bool(int(sys.argv[5]))

	central_force = True
	if len(sys.argv) > 6:
		central_force = bool(int(sys.argv[6]))

	generate(filename, grid_dimension, max_value, wrap, checkerboard, central_force)
