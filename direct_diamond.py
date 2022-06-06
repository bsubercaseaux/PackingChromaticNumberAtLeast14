from itertools import islice
from functools import partial
import sys


V = {}
IV = {}


def clause_to_text(clause):
	return " ".join(map(str, clause + [0]))

def write_to_file(clauses, filename):
	with open(filename, 'w') as file:
		file.write(f"p cnf {len(V)} {len(clauses)}\n")
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

def exact_k_vdirs(k):
	vdirs = vdirs_k(k)
	def filt(vdir):
		i, j = vdir
		return abs(i) + abs(j) == k
	return list(filter(filt, vdirs))

def first_eighth(vdir):
	i, j = vdir
	return i >=0 and j >= 0 and j <= i


def eight_separate(vdirs):
	return list(filter(first_eighth, vdirs)), list(filter(lambda x: not first_eighth(x), vdirs))

def partition(seq, parts):
	return list(iter(partial(lambda it: tuple(islice(it, parts)), iter(seq)), ()))

def generate(filename, radius, max_value, symmetry_breaking, central_force=True):
	clauses = []
	## clauses for each position having at least a color!
	for i in range(-radius, radius+1):
		for j in range(-radius, radius+1):
			if abs(i) + abs(j) <= radius:
				clause = []
				for k in range(1, max_value+1):
					V[(i, j, k)] = len(V)+1
					IV[V[(i, j, k)]] = (i,j,k)
					clause.append(V[(i,j,k)])
				clauses.append(clause)


	## clauses forbidding x_{i,j,v} and x_{a,b,v} if dist(i, j, a, b) <= v.
	for number in range(1, max_value+1): 
		vdirs = vdirs_k(number)
		for i in range(-radius, radius+1):
			for j in range(-radius, radius+1):
				if abs(i) + abs(j) > radius: continue
				for vdir in vdirs:
					di, dj = vdir
					new_i, new_j = i+di, j +dj
					if abs(new_i) + abs(new_j) > radius:
							continue	
					clauses.append([-V[(i, j, number)], -V[(new_i, new_j, number)]])
	if central_force:	
		if max_value != 15:
			clauses.append([V[(0,0, min(radius, max_value))]])
		else:
			clauses.append([V[(0,0,max_value)]])

	# break symmetry by forcing radius+1 being on a particular eighth
	if symmetry_breaking:
		for r in range(1, radius+1):
			V[r] = len(V) + 1
			IV[V[r]] = r
		
		for r in range(1, radius):
			clauses.append([-V[r], V[r+1]])

		for r in range(1, radius+1):
			# if (BIGOR  x_{r}) -> V[r]
			ek_vdirs = exact_k_vdirs(r)
			for vdir in ek_vdirs:
				i,j = vdir
				clauses.append([-V[(i,j, max_value)], V[r]])
			

		for r in range(1, radius+1):
			# if ~V[r] -> (V(no eighth) -> V(eighth))
			 # V[r] v (V no eight -> V eight)
				# V[r] v V[eight] v (~ no eight_1) ^ V[r] v V[eight] v (~ no eight_2) ^ ...
			r_clauses = []
			ek_vdirs =  exact_k_vdirs(r)
			eight, no_eight = eight_separate(ek_vdirs)
			
			base_clause = []
			if r > 1:
				base_clause.append(V[r-1])
			for vdir in eight:
				i,j = vdir
				base_clause.append(V[(i,j, max_value)])
			for vdir in no_eight:
				i,j = vdir
				r_clauses.append(base_clause + [-V[(i,j, max_value)]])
			clauses.extend(r_clauses)
	only_center = False
	if only_center:
		for pos in vdirs_k(radius):
			i, j = pos
			clauses.append([-V[(i, j, max_value)]])
		
	write_to_file(clauses, filename)
	print(f"# variables = {len(V)}, # clauses = {len(clauses)}")

if len(sys.argv) > 4:
	
	filename = sys.argv[1]

	radius = int(sys.argv[2])
	max_value = int(sys.argv[3])
	
	symmetry_breaking = bool(int(sys.argv[4]))

	central_force = True
	if len(sys.argv) > 5:
		central_force = bool(int(sys.argv[5]))


	generate(filename, radius, max_value, symmetry_breaking, central_force)
