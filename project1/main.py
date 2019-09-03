import math
import time
from operator import itemgetter

# goal_state = [1, 2, 3, 4, 5, 6, 7, 8, -1]

trivial = [1, 2, 3, 4, 5, 6, 7, 8, -1]
           
very_easy = [1, 2, 3, 4, 5, 6, 7, -1, 8]
            
easy = [1, 2, -1, 4, 5, 3, 7, 8, 6]
        
doable = [-1, 1, 2, 4, 5, 3, 7, 8, 6]
          
oh_boy = [8, 7, 1, 6, -1, 2, 5, 4, 3]

# debug if a solution is found for this one
impossible = [1, 2, 3, 4, 5, 6, 8, 7, -1]

N_PUZZLE = 8 # N indicates what puzzle it is; i.e. 8, 15, 24, etc.
SIZE_OF_MATRIX = int(math.sqrt(N_PUZZLE + 1))

class priority_queue(object):

    def __init__(self):
        self.elements = []
        self.max_elements = 0

    def get_max_elements(self):
    	return self.max_elements
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, h=0, g=0, priority=0):
        self.elements.append((priority, h, g, item))
        self.elements.sort(key=itemgetter(0))
        self.max_elements = self.max_elements if self.max_elements > len(self.elements) else len(self.elements)

    def get_item(self):
        return self.elements.pop(0)

class Problem(object):

	def __init__(self, initial_state=None):
		self.initial_state = initial_state
		self.goal_state = self.get_goal()
		self.explored = []

	def goal_test(self, node):
		self.explored.append(node)
		return node == self.goal_state

	def get_level(self):
		return len(self.explored);

	def is_explored(self, node):
		return node in self.explored

	def get_current_state(self):
		return self.initial_state

	def get_goal_state(self):
		return self.goal_state

	def get_goal(self):
		goal = []
		for x in range(1, N_PUZZLE + 1):
			goal.append(x)
		goal.append(-1)
		return goal

	def print_current_board(self):
		print_board(self.initial_state)

# prints current state of board
def print_board(mat):
	# print("\nPUZZLE LOOKS LIKE:")
	print("\n")
	# print("*" * 5 * SIZE_OF_MATRIX)
	for index, val in enumerate(mat):
		if (index + 1) % SIZE_OF_MATRIX == 0:
			print(val if val != -1 else "x")
		else:
			print(val if val != -1 else "x", " ", end=' ')
	# print("*" * 5 * SIZE_OF_MATRIX)

# checks if you can move up
def can_move_up(mat):
	return True if mat.index(-1) >= SIZE_OF_MATRIX else False

# checks if you can move down
def can_move_down(mat):
	return True if mat.index(-1) < N_PUZZLE + 1 - SIZE_OF_MATRIX else False

# checks if you can move to the left
def can_move_left(mat):
	return False if mat.index(-1) % SIZE_OF_MATRIX == 0 else True

# checks if you can move to the right
def can_move_right(mat):
	return False if mat.index(-1) % SIZE_OF_MATRIX == SIZE_OF_MATRIX - 1 else True

# moves the blank space up
def move_blank_up(mat):
	if can_move_up(mat):
		index = mat.index(-1)
		mat[index - SIZE_OF_MATRIX], mat[index] = mat[index], mat[index - SIZE_OF_MATRIX]
		return mat
	return None

# moves the blank space down
def move_blank_down(mat):
	if can_move_down(mat):
		index = mat.index(-1)
		mat[index + SIZE_OF_MATRIX], mat[index] = mat[index], mat[index + SIZE_OF_MATRIX]
		return mat
	return None

# moves the blank space to the left
def move_blank_left(mat):
	if can_move_left(mat):
		index = mat.index(-1)
		mat[index - 1], mat[index] = mat[index], mat[index - 1]
		return mat
	return None

# moves the blank space to the right
def move_blank_right(mat):
	if can_move_right(mat):
		index = mat.index(-1)
		mat[index + 1], mat[index] = mat[index], mat[index + 1]
		return mat
	return None

# the generic search algorithm from slides
def general_search(problem, queueing_func):
	depth = 0
	nodes = priority_queue()
	nodes.put(problem.get_current_state())
	while not nodes.empty():
		entire_node = nodes.get_item()
		node = entire_node[3]
		if (entire_node[2] or entire_node[1]):
			print("The best state to expand with a g(n) = %d and h(n) = %d is..." % (entire_node[2], entire_node[1]), end=' ')
		print_board(node)
		if problem.goal_test(node): 
			print("\nThe goal state was reached!")
			print("Number of nodes expanded to solve puzzle with this algorithm: %d" % problem.get_level())
			print("Max. number of nodes in queue: %d"% nodes.get_max_elements())
			print("Goal node depth: %d" % entire_node[2])
			return node
		print("Expanding state...\n")
		print("\n")
		queueing_func(nodes, expand(entire_node, problem))
		depth += 1
	
# expanding current node via moving up/down/left/right
def expand(node, problem):
	all_nodes = priority_queue()
	node1 = move_blank_up(node[3][:])
	node2 = move_blank_down(node[3][:])
	node3 = move_blank_left(node[3][:])
	node4 = move_blank_right(node[3][:])
	if node1 and not problem.is_explored(node1):
		all_nodes.put(node1, 0, node[2] + 1, 0)
	if node2 and not problem.is_explored(node2):
		all_nodes.put(node2, 0, node[2] + 1, 0)
	if node3 and not problem.is_explored(node3):
		all_nodes.put(node3, 0, node[2] + 1, 0)
	if node4 and not problem.is_explored(node4):
		all_nodes.put(node4, 0, node[2] + 1, 0)
	return all_nodes

# uniform cost search queuing function
def uniform_cost_search(nodes, new_nodes):
	while not new_nodes.empty():
		node = new_nodes.get_item()
		nodes.put(node[3], 0, node[2], 0)

# heuristic calculation via Misplaced Tile
def calculate_misplaced(node):
	count = 0
	for i in range(N_PUZZLE):
		if i+1 != node[i]:
			count += 1
	return count

# heuristic calculation via Manhattan Distance
def manhattan_distance(node):
	count = 0
	for i in range(N_PUZZLE):
		index = node.index(i + 1)
		row_diff = abs((i / SIZE_OF_MATRIX) - (index / SIZE_OF_MATRIX))
		col_diff = abs((i % SIZE_OF_MATRIX) - (index % SIZE_OF_MATRIX))
		count += (row_diff + col_diff)
	index = node.index(-1)
	row_diff = abs((N_PUZZLE / SIZE_OF_MATRIX) - (index / SIZE_OF_MATRIX))
	col_diff = abs((N_PUZZLE % SIZE_OF_MATRIX) - (index % SIZE_OF_MATRIX))
	count += (row_diff + col_diff)
	return count

# Misplaced Tile heuristic search queuing function
def misplaced_tile_heuristic(nodes, new_nodes):
	while not new_nodes.empty():
		node = new_nodes.get_item()
		nodes.put(node[3], calculate_misplaced(node[3]), node[2], calculate_misplaced(node[3]) + node[2])

# Misplaced Tile heuristic search queuing function
def manhattan_distance_heuristic(nodes, new_nodes):
	while not new_nodes.empty():
		node = new_nodes.get_item()
		nodes.put(node[3], manhattan_distance(node[3]), node[2], manhattan_distance(node[3]) + node[2])

# main function ft. home menu
if __name__ == "__main__":
	print("Welcome to the %d-Puzzle Solver!" % N_PUZZLE)
	print("Enter \"1\" to use a default puzzle, or \"2\" to enter your own puzzle.")
	choice = int(input())
	mat = []
	if choice == 1:
		print("Want to use a default puzzle? Choose from the following:\n1. Trivial\n2. Very Easy\n3. Easy\n4. Doable\n5. Oh Boy\n6. Impossible")
		default_puzzle_choice = int(input())
		if default_puzzle_choice == 1:
			mat = trivial
		elif default_puzzle_choice == 2:
			mat = very_easy
		elif default_puzzle_choice == 3:
			mat = easy
		elif default_puzzle_choice == 4:
			mat = doable
		elif default_puzzle_choice == 5:
			mat = oh_boy
		elif default_puzzle_choice == 6:
			mat = impossible
	elif choice == 2:
		print("Enter your %d-Puzzle." % N_PUZZLE)
		print("Type \"x\" for the blank space.\n")
		for i in range(SIZE_OF_MATRIX):
			print("Enter elements for row %d:" % (i + 1))
			mat.extend([-1 if x == "x" else int(x) for x in input().split()])
			print("\n")

	problem = Problem(mat)
	print("Initial state", end=' ')
	problem.print_current_board()
	print("\n")
	print("Goal state", end=' ')
	print_board(problem.get_goal_state())
	print("\n")
	# print("*"*50)
	print("Enter your choice of algorithm:\n1. Uniform Cost Search\n2. A* with the Misplaced Tile heuristic.\n3. A* with the Manhattan Distance heuristic.")
	choice = int(input())
	# t1 = 0
	if choice == 1:
		# t1 = time.time()
		general_search(problem, uniform_cost_search)
	elif choice == 2:
		# t1 = time.time()
		general_search(problem, misplaced_tile_heuristic)
	elif choice == 3:
		# t1 = time.time()
		general_search(problem, manhattan_distance_heuristic)
	else:
		print("Try again!")
	# t2 = time.time()
	# print("Time: " + str((t2-t1) * 1000)  + " ms")