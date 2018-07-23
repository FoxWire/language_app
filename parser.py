import os
from nltk.parse import stanford
import nltk
from scipy.spatial import distance


class Comparer():
	'''
	This class compares based on the frequency distribution method. 
	This was the first attempt. It compares naively based on the number of 
	specific label in the vector. It doesn't take the structure of the 
	tree into consideration.
	'''

	def __init__(self):
		self.parser = stanford.StanfordParser()
		self.syncats = self._get_syncats()


	def _get_syncats(self):
		# Get a list of the syntactic categories
		with open('new_markers.txt', 'r') as input:
			return [line.strip() for line in input]

	def _get_freq_dest(self, labels):

		# Create the feature set based on the frequency distribution
		freq_dist = nltk.FreqDist()
		for label in labels:
			freq_dist[label] += 1

		feature_set = {}
		for cat in self.syncats:
			feature_set[cat] = freq_dist[cat]

		return feature_set

	def _get_difference(self, vector_a, vector_b):
		return distance.cosine(vector_a, vector_b)	


	def compare(self, labels_a, labels_b):

		feature_set = self._get_freq_dest(labels_a)	
		vector_a = [val for val in feature_set.values()]

		feature_set = self._get_freq_dest(labels_b)	
		vector_b = [val for val in feature_set.values()]

		return self._get_difference(vector_a, vector_b)


class TreeComparer():
	'''
	This class uses the zzs algorithm to work out the similarity between 
	two trees.
	'''

	def __init__(self):
		self.parser = stanford.StanfordParser()


	def convert_parse_tree_to_python_tree(tree_as_list):
	    tree_as_list = tree_as_list[2:-1]
	    stack = [ ['ROOT', []],  ]
	    root = stack[0]
	    # Iterate over the list
	    for i, item in enumerate(tree_as_list):
	        if item == '(':

	            # If the node doesn't have children
	            match = re.search(r'[A-Z]+[ ][A-Za-z]+', tree_as_list[i + 1])
	            if match:
	                label = match.group().split(' ')
	                node = [label[0], label[1]]
	            else:
	                node = [tree_as_list[i + 1], []]

	            # Add the node to the children of the current item
	            stack[-1][1].append(node)
	            # Then add the node to the stack itself
	            stack.append(node)
	        elif item == ')':
	            # this node has no children so just pop it from the stack
	            stack.pop()
	    return root


	def convert_parse_tree_to_zss_tree(tree_as_list):
	    tree_as_list = tree_as_list[2:-1]
	    stack = [Node('ROOT')]
	    root_node = stack[0]
	    # Iterate over the list
	    for i, item in enumerate(tree_as_list):
	        if item == '(':
	            # match the string for each item 
	            match = re.search(r'[A-Z]+[ ][A-Za-z]+', tree_as_list[i + 1])
	            if match:
	                # if match, node has no children
	                label = match.group().split(' ')
	                node = Node(label[0]).addkid(Node(label[1]))
	            else:
	                # otherwise node has children
	                node = Node(tree_as_list[i + 1])
	            # Add the node to the children of the current item
	            stack[-1].addkid(node)
	            # Then add the node to the stack itself
	            stack.append(node)
	        elif item == ')':
	            # this node has no children so just pop it from the stack
	            stack.pop()
	    return root_node




