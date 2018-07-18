import os
from nltk.parse import stanford
import nltk
from scipy.spatial import distance

# parser = stanford.StanfordParser()

# Get a list of the syntactic categories
# with open('new_markers.txt', 'r') as input:
# 	syncats = [line.strip() for line in input]

# def get_labels(sentence):

# 	# Create parse tree and get a list of all the labels from it
# 	parse_tree = parser.raw_parse(sentence)
# 	labels = []
# 	for x in parse_tree:
# 		for sub in x.subtrees():
# 			labels.append(sub.label())
# 	return labels

# def get_freq_dest(labels):

# 	# Create the feature set based on the frequency distribution
# 	freq_dist = nltk.FreqDist()
# 	for label in labels:
# 		freq_dist[label] += 1

# 	feature_set = {}
# 	for cat in syncats:
# 		feature_set[cat] = freq_dist[cat]

# 	return feature_set

# def get_difference(vector_a, vector_b):

# 	# Work out the differnce between the two vectors
# 	for cat, a, b in zip(syncats, vector_a, vector_b):
# 		print(cat, '\t',  a, b)
# 	print('')

# 	return distance.cosine(vector_a, vector_b)	


class Comparer():

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


# sentence_a = "I'm looking forward to seeing you next weekend."
# sentence_b = "I am looking forward to flying to Canada next year."

# feature_set = get_freq_dest(get_labels(sentence_a))	
# vector_a = [val for val in feature_set.values()]

# feature_set = get_freq_dest(get_labels(sentence_b))	
# vector_b = [val for val in feature_set.values()]

# print('difference:', get_differnce(vector_a, vector_b))

