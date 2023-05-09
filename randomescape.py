from collections import defaultdict
import itertools

def get_box_vars(dimensions):
	locs = list(itertools.product(*[range((-dim // 2) + 1, (dim // 2) + 1) for dim in dimensions]))
	steps = get_steps(len(dimensions))
	neighbors = get_neighbors(locs, steps)
	start = (0,) * len(dimensions)
	probs = get_probs(locs, start)
	return (locs, steps, neighbors, start, probs)

def get_steps(num_dimensions):
	steps = []
	for i in range(num_dimensions):
		steps += [(0,) * i + (1,) + (0,) * (num_dimensions - i - 1)]
		steps += [(0,) * i + (-1,) + (0,) * (num_dimensions - i - 1)]
	return steps

def get_probs(locs, start):
	probs = {'escape': 0}
	for loc in locs:
		probs[loc] = 1 if loc == start else 0

	return probs

def get_neighbors(locs, steps):
	neighbors = {}
	for loc in locs:
		neighbors[loc] = []
		for step in steps:
			neighbor = tuple(start + move for start, move in zip(loc, step))
			if neighbor in locs:
				neighbors[loc].append(neighbor)
			else:
				neighbors[loc].append('escape')

	return neighbors

box_dims = [3, 3]
locs, steps, neighbors, start, probs = get_box_vars(box_dims)

steps = 0
expected_steps = 0
multiplier = 1 / len(neighbors[start])

while probs['escape'] < 1 - 1e-12: 
	newProbs = defaultdict(lambda: 0)
	for loc in locs:
		loc_neighbors = neighbors[loc]
		for loc_neighbor in loc_neighbors:
			newProbs[loc_neighbor] += multiplier * probs[loc]

	steps += 1
	expected_steps += steps * (newProbs['escape'])
	newProbs['escape'] += probs['escape']
	probs = newProbs
	if (steps & (steps - 1)) == 0:
		print ("At step: " + str(steps) + " there is probability " + f"{probs['escape']:.10f}" + " of having escaped.")
		

print ("Expected steps to escape: " + str(expected_steps))



