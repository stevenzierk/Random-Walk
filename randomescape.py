from collections import defaultdict
import itertools
import numpy as np

def get_box_vars(dimensions):
	locs = list(itertools.product(*[range((-dim // 2) + 1, (dim // 2) + 1) for dim in dimensions]))
	steps = get_steps(len(dimensions))
	neighbors = get_neighbors(locs, steps)
	start = (0,) * len(dimensions)
	probs = get_probs(locs, start)
	return (locs, neighbors, start, probs)

def get_shape_vars(locs):
	num_dimensions = len(locs[0])
	steps = get_steps(num_dimensions)
	neighbors = get_neighbors(locs, steps)
	start = (0,) * num_dimensions
	probs = get_probs(locs, start)
	return (locs, neighbors, start, probs)

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

def calculate_escape_e(locs, neighbors, start, probs):
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
			print ("At step " + str(steps) + " there is probability " + f"{probs['escape']:.10f}" + " of having escaped.")
			
	print ("Total steps run: " + str(steps))
	print ("Expected steps to escape: " + str(expected_steps))

	return expected_steps

def develop_markov_matrix(locs, neighbors):
	markov_matrix = [[0 for i in range(len(locs))] for j in range(len(locs))]
	states_map = {value: index for index, value in enumerate(locs)}
	multiplier = 1 / len(neighbors[locs[0]])

	for loc in locs:
		for neighbor in neighbors[loc]:
			if neighbor != 'escape':
				row, col = states_map[loc], states_map[neighbor]
				markov_matrix[row][col] += multiplier

	return markov_matrix 


LOCS_P1 = [(-3, 2), (3, 2), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (-1, -1), (0, -1), (1, -1), (-1, -2), (0, -2), (1, -2), (-1, -3), (0, -3), (1, -3)]


#box_dims = [5, 5]
#locs, neighbors, start, probs = get_box_vars(box_dims)
#calculate_escape_e(locs, neighbors, start, probs)

locs = LOCS_P1
locs, neighbors, start, probs = get_shape_vars(locs)

num_locs = len(locs)
markov_matrix = np.array(develop_markov_matrix(locs, neighbors))
fundamental_matrix = np.linalg.inv(np.eye(num_locs) - markov_matrix)
expectations = np.matmul(fundamental_matrix, np.ones((num_locs, 1)))
for loc, expectation in zip(locs, expectations):
	print (loc, expectation)


