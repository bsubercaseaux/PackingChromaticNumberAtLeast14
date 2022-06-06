import sys
import functools
import itertools
import random
import math

filename = sys.argv[1]
radius = int(sys.argv[2])
colors = int(sys.argv[3])
forces = int(sys.argv[4])
symmetry_breaking = bool(int(sys.argv[5]))
d_value = int(sys.argv[6])

split = 1
if len(sys.argv) > 7:
	split = int(sys.argv[7])

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

positions = vdirs_k(d_value)
semantic_lst = []
cubes = []
forced_colors = []


for i in range(colors, 0, -1):
	if i != min(radius, colors) and len(forced_colors) < forces:
		forced_colors.append(i)
	
# print(f"positions = {len(positions)}")
n_cubes = 0
for f in range(forces, -1, -1):
	for pos_tuple in itertools.combinations(positions, f):
		pos_set = set(list(pos_tuple))
		for color_comb in itertools.permutations(forced_colors, f):
			cube = []
			color_lst = list(color_comb)
			
			if symmetry_breaking and len(color_lst) > 0:
				mx_clr = max(color_lst)
				idx_mx_clr = color_lst.index(mx_clr)
				pos_mx_clr = pos_tuple[idx_mx_clr]
				
				x, y = pos_mx_clr
				# skip if outside the main eighth
				if x < 0 or y < 0 or y > x:
					continue	
					
	
			for i, tup in enumerate(pos_tuple):
				x, y = tup
				cube.append(V[(x, y, color_lst[i])])
			taut = True
			if taut:
				for pos in positions:
					if pos in pos_set: continue
					x, y = pos
					for color in forced_colors:
						if color not in color_lst:
							cube.append(-V[(x, y, color)])
				assert len(cube) == f+(forces-f)*(len(positions)-f)
			n_cubes += 1
			#if n_cubes % 1000 == 0:
			#	print(f"n_cubes = {n_cubes}")
			cubes.append(cube)

# last cubes symmetry breaking.
last_cube_decomposition = False
if last_cube_decomposition:
	next_colors = range(colors-forces-1, 0,-1)
	last_cube_decomposition = 3
	for i in range(last_cube_decomposition):
		for pos in positions:
			x, y = pos
			cube = []	
			if symmetry_breaking:
				if x < 0 or y < 0 or y > x: continue
			cube.append(V[(x, y, next_colors[i])])
			for color in forced_colors + list(next_colors[:i]):
				for pos in positions:
					x, y = pos
					cube.append(-V[(x, y, color)])						
			cubes.append(cube)
	
	# very last cube:
	cube = []
	for pos in positions:
		x, y = pos
		for color in forced_colors + list(next_colors[:last_cube_decomposition]):
			cube.append(-V[(x, y, color)])
	cubes.append(cube)
		

def last_actual_cubes(origin_filename, out, n_last_cube=1):
	with open(origin_filename, 'r') as origin:
		header = origin.readline()
		words = header.split(" ")
		vrs, n_clauses = int(words[2]), int(words[3])
		content = origin.read()
	with open(out, 'w') as cubes_file:
		cube = cubes[-n_last_cube]
		cubes_file.write(f"p cnf {vrs} {n_clauses + len(cube)}\n")
		cubes_file.write(content)
		for lit in cube:
			cubes_file.write(f"{lit} 0\n")

def generate_last_cube_file(origin_filename, out):
	with open(origin_filename, 'r') as origin:
		header = origin.readline()
		words = header.split(" ")
		vrs, n_clauses = int(words[2]), int(words[3])
		content = origin.read()
	with open(out, 'w') as cubes_file:
		cubes_file.write(f"p cnf {vrs} {n_clauses + len(cubes)}\n")
		cubes_file.write(content)
		for i, cube in enumerate(cubes):
			n_cube = map(lambda x: -x, cube)
			str_cube = map(str, n_cube)
			cubes_file.write(f"{' '.join(str_cube)} 0\n")

def generate_tautology_file(origin_filename, out):
	with open(origin_filename, 'r') as origin:
		header = origin.readline()
		words = header.split(" ")
		vrs, n_clauses = int(words[2]), int(words[3])
		content = origin.read()
	with open(out, 'w') as cubes_file:
		cubes_file.write(f"p cnf {vrs} {len(cubes)}\n")
		for i, cube in enumerate(cubes):
			n_cube = map(lambda x: -x, cube)
			str_cube = map(str, n_cube)
			cubes_file.write(f"{' '.join(str_cube)} 0\n")


lst = list(map(lambda x: V[x], semantic_lst))

def neg_last(lst):
	cp = list(lst)
	cp[-1]*=-1
	return cp

def neg_by_indices(lst, indices):
	cp = list(lst)
	for i in indices:
		cp[i] *= - 1
	return cp

def cubes_by_k_tuple(lst, k):
	cubes = [lst]
	n = len(lst)
	for i in range(n-k+1):
		# ending in position n-1-i.
		slst = list(lst[:n-i])
		for cmb in itertools.combinations(range(n-1-i), k-1):
			triple = [n-1-i] + list(cmb)
			cubes.append(neg_by_indices(slst, triple))
	return cubes
		
def gen_cube_files(origin_filename, out, split=1):
	with open(origin_filename, 'r') as origin:
		header = origin.readline()
		words = header.split(" ")
		vrs, n_clauses = int(words[2]), int(words[3])
		content = origin.read()
	buffers = [[] for _ in range(split)]
	for i in range(split):
		buffers[i].append("p inccnf\n")
		buffers[i].append(content)
	
	for i in range(len(cubes)):
		cube = cubes[i]
		buffers[i%split].append(f"a {' '.join(list(map(str, cube)))} 0\n")
	
	sb = ""
	if symmetry_breaking:
		sb = "SB"
	for i in range(split):
		with open(f"split-{origin_filename}-{d_value}-{forces}-{sb}-{i}.icnf",'w') as cube_file:
			cube_file.write(''.join(buffers[i]))

def gen_specific_cube_files(origin_filename, list_of_cubes):
	with open(origin_filename, 'r') as origin:
		header = origin.readline()
		words = header.split(" ")
		vrs, n_clauses = int(words[2]), int(words[3])
		content = origin.read()
	for i, cube in enumerate(list_of_cubes):
		with open(f"sp-{cube}-{origin_filename}", 'w') as out:
			out.write(f"p cnf {vrs} {n_clauses+1}\n")
			out.write(content)
			out.write(f"{' '.join(list(map(str, cubes[cube])))} 0\n")
			

print(f"number of cubes = {len(cubes)}")
gen_cube_files(filename, f"cubes-{filename}", split)
#gen_specific_cube_files(filename, [812826, 812827, 812830])
#generate_last_cube_file(filename, f"last-cube-{filename}")
#generate_tautology_file(filename, f"taut-check-{filename}")
#last_actual_cubes(filename, f"last-actual-cubes-{filename}", 3)
