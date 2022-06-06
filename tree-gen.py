levels = 9

vertices = 2**levels-1

G = [[] for v in range(vertices)]

for v in range(vertices):
	lchild = 2*v + 1
	rchild = 2*v + 2
	if max(lchild, rchild) > vertices:
		break
	G[v].append(lchild)
	G[v].append(rchild)
	G[lchild].append(v)
	G[rchild].append(v)

print(vertices)
for v in range(vertices):
	print(" ".join(map(str,[v] + G[v])))
