import sys
import math

class RecursiveGenerator:
	def __init__(self, grid_dimension : int, max_value : int) -> None:
		self.V = {}
		self.IV = {}
		self.clauses = []
		self.gd = grid_dimension
		self.mv = max_value
		
		# build powers of two:
		self.powers_of_two = [2**k for k in range(math.ceil(math.log2(self.mv)))]
	
	def c_var(self, i, j, v, pw):
		return self.V[f"P_{(i+self.gd)%self.gd, (j+self.gd)%self.gd, v, pw}"]

	# construction of the powers of two in terms of smaller variables!
	# P_{i,j,v,k} -> P_{,,v,k-1} and ... (4 of those!)
	def power_decomposition_clauses(self, i, j, v, pw):
		V = self.V
		gd = self.gd
		answer = []
		vdirs = [(-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)]
		
		if pw == 1:
			for vdir in vdirs:
				di, dj = vdir
				answer.append([-1*self.c_var(i, j, v, pw), -1*V[f"X_{ (i+di+gd)%gd,  (j+dj+gd)%gd,v}"]])
			return answer
		for vdir in vdirs:
			di, dj = vdir
			answer.append([-1*self.c_var(i, j, v, pw), self.c_var(i + di*pw//2, j + dj*pw//2, v, pw//2)])
		return answer



	# takes a tuple (i, j, v) and a radius r
	# returns clauses enforcing that no value v is assigned to the ball
	# B((i, j), r)
	def whole_decomposition(self, i, j, v, r):
		if r in self.powers_of_two:
			return [[self.c_var(i, j, v, r)]]
		pw = 1
		while pw < r:
			pw *= 2
		pw //=2
		# pw is now the largest power of 2 that is smaller than r (and greater than r/2)!
		clauses = []
		vdirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
		for vdir in vdirs:
			di, dj = vdir
			clauses.append([self.c_var(i+di*(r-pw), j+dj*(r-pw), v, pw)])
		return clauses
				
	# returns all directing vectors at l_1 distance <= k but > 0
	## equivalent to l_1 distance-bounded BFS, but easier to write and more efficient.
	@staticmethod
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

	# receives (i,j,v) and blocks occurrences of v in the ball B((i,j), v) \ (i,j).
	def hollow_center_decomposition(self, i, j, v):
		gd = self.gd
		V = self.V
		if v < 3:
			# manually
			clauses = []
			vdirs = RecursiveGenerator.vdirs_k(v)
			for vdir in vdirs:
				di, dj = vdir
				clauses.append([-1*V[f"X_{ (i+di+gd)%gd, (j+dj+gd)%gd,v}"]])
			return clauses
		else:
			# the 8 clauses of death (?) (4 orthogonal + 4 diagonals)
			clauses = []
			main_vdirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
			## 4 orthogonal ones
			for vdir in main_vdirs:
				di, dj = vdir
				clauses.extend(
					self.whole_decomposition(
						i + di*(v//2 + 1),
						j + dj*(v//2 + 1),
						v, 
						(v-1)//2)
				)
		
			secondary_vdirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
			## 4 Barcelona ones
			### takes care of parity by alternating between upper/lower rounding of the midpoint of each diagonal
			lower_half = math.floor((v//2+1)/2)
			upper_half = math.ceil((v//2+1)/2)
			halves = [lower_half, upper_half]
			for idx, vdir in enumerate(secondary_vdirs):
				di, dj = vdir
				clauses.extend(
					self.whole_decomposition(
						i + di*halves[idx%2],
						j + dj*halves[(idx+1)%2],
						v, 
						(v-1)//2)
				)

			if v % 2 == 0: 
				# I should include a proof that this is only required for even values
				# we enforce the 4 orthogonally adjacent cells
				for vdir in main_vdirs:
					di, dj = vdir
					clauses.append([-1*V[f"X_{(i+di+gd)%gd,(j+dj+gd)%gd,v}"]])
				
			return clauses

	@staticmethod
	def clause_to_text(clause):
		return " ".join(map(str, clause + [0]))


	def write_to_file(self, filename):
		with open(filename, 'w') as file:
			file.write(f"p cnf {len(self.V)} {len(self.clauses)}\n")
			for clause in self.clauses:
				file.write(RecursiveGenerator.clause_to_text(clause) + '\n')
		print(f"# vars = {len(self.V)}, # clauses = {len(self.clauses)}")

	def generate(self, guide=None):
		gd = self.gd 
		mv = self.mv
		V = self.V
		IV = self.IV
		for i in range(gd):
			for j in range(gd):
				for v in range(1, mv+1):
					V[f"X_{i,j,v}"] = len(V) + 1
					IV[V[f"X_{i,j,v}"]] = f"X_{i,j,v}"

		# clauses for each position having at least a color!
		for i in range(gd):
			for j in range(gd):
				self.clauses.append([V[f"X_{i,j,v}"] for v in range(1, mv+1)])

		
		recursive_start = 5


		# build variables
		for i in range(gd):
			for j in range(gd):
				for v in range(recursive_start, mv+1):
					for k, pw in enumerate(self.powers_of_two):
						if pw > v: break
						V[f"P_{i, j, v, pw}"] = len(V) + 1
						IV[V[f"P_{i,j,v,pw}"]] = f"P_{i,j,v,pw}"

		
		
		# recursive decompositions of powers of two
		for i in range(gd):
			for j in range(gd):
				for v in range(recursive_start, mv+1):
					for k, pw in enumerate(self.powers_of_two):
						if pw > v: break
						self.clauses.extend(self.power_decomposition_clauses(i, j, v, pw))

		# generate forbidding clauses
		for i in range(gd):
			for j in range(gd):
				for v in range(recursive_start, mv+1):
					forbidden_unitary_clauses = self.hollow_center_decomposition(i, j, v)
					for cls in forbidden_unitary_clauses:
						forbidden_var = cls[0]
						self.clauses.append([-1*V[f"X_{i,j,v}"], forbidden_var])

		# Force checkerboard of ones:
		for i in range(gd):
			for j in range(gd):
				if (i+j)%2 == 0:
					self.clauses.append([V[f"X_{i,j,1}"]])
		#guide = [(5,6)]		
		if guide is not None:
			for guide_cell in guide:
					i, j, val = guide_cell
					self.clauses.append([V[f"X_{i,j,val}"]])

## ------- FOR TESTING STUFF MANUALLY --------------------
### pretty printing
def pprint_clause(clause, IV):
	lclause = []
	for var in clause:
		if var < 0:
			lclause.append(f"(not {IV[-1*var]})")
		else:
			lclause.append(f"{IV[var]}")
	print(" or ".join(lclause))

def pprint_clauses(clauses):
	for clause in clauses:
		pprint_clause(clause)

### ------------------------------------------

## python3 recursive.py <grid_dimension> <max_value> [<filename>]
if len(sys.argv) > 3:
	filename = sys.argv[1]
	grid_dimension = int(sys.argv[2])
	max_value = int(sys.argv[3])

	generator = RecursiveGenerator(grid_dimension, max_value)
	generator.generate()
	generator.write_to_file(filename)

