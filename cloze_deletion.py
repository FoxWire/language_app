import os
from nltk.parse import stanford
import nltk
from scipy.spatial import distance
import re
import json

# def cloze_deletion(sentence_a, sentence_b):
# 	# start by parsing both tree
# 	tree_a = next(parser.raw_parse(sentence_a))
# 	prods_a = [str(p) for p in tree_a.productions() if not re.search(r'[\'a-z\']+', str(p))]

# 	tree_b = next(parser.raw_parse(sentence_b))
# 	prods_b = [str(p) for p in tree_b.productions() if not re.search(r'[\'a-z\']+', str(p))]

# 	similar_prods = []
# 	for a, b in zip(prods_a, prods_b):
# 		if a == b:
# 			similar_prods.append(a)


# def get_index_of_subtree(tree, subtree):
# 	# Finds the index of the specified subtree within the 
# 	# specified tree.
# 	index = None
# 	for position in tree.treepositions():
# 		if tree[position] == subtree:
# 			index = position
# 	return index

# def strip_leaves(tree):
# 	'''
# 	Returns a tree with the leaves removed. 
# 	'''
# 	s = str(tree)
# 	stripped = re.sub(r'[A-Z]{1}[a-z]+', "", s)
# 	stripped = re.sub(r'[a-z]+', "", stripped)
# 	stripped = re.sub('I', "", stripped)

# 	if 'ROOT' in stripped:
# 		stripped = re.sub('ROOT', "", stripped)
# 		stripped = stripped[1:-1]
# 	return nltk.tree.Tree.fromstring(stripped)

# def compare_on_structure(tree_a, tree_b):
# 	return strip_leaves(tree_a) == strip_leaves(tree_b)


# tree_a = next(parser.raw_parse("I have a big dog"))
# tree_b = next(parser.raw_parse("I am looking forward to seeing you at the weekend"))

# nested = strip_leaves(tree_a)
# for sub in tree_b.subtrees():
# 	if strip_leaves(sub) == nested:
# 		index = get_index_of_subtree(tree_b, sub)
# 		tree_b[index] = tree_a
# tree_b.pretty_print()


# tree_a.pretty_print()	
# tree_b.pretty_print()	


# attempt to remove tree a from tree b 
# index = get_index_of_subtree(tree_b, tree_a)
# print(index)
# del tree_b[index]
# tree_b.pretty_print()

# print(list(tree_b.subtrees()))
# for sub in tree_b.subtrees():
# 	print(sub.flatten())
	

'''
This script works out which phrases (combinations of words in the sentence should be used for the closed deletions.
It creates a parse tree of the sentence and then creates a list of tuples for each of the subtrees in the parse tree.
The first part of the tuple is the label, that representes the root of the parse tree, you can get this by flattening
three and taking the label.
Now that the sentences are in this format, we can take the cross reference the labels with the higher up (in the tree)
labels that we want to keep. Next we just need to filter out the ones that are one word or the whole sentence.

There is some code above here that I origianlly started with. It might still be useful for something at a later
point.
'''

# Now you need to get a list of the clause and phrase labels
text = '''
S - simple declarative clause, i.e. one that is not introduced by a (possible empty) subordinating conjunction or a wh-word and that does not exhibit subject-verb inversion.
SBAR -ADJP - Adjective Phrase.
ADVP - Adverb Phrase.
CONJP - Conjunction Phrase.
FRAG - Fragment.
INTJ - Interjection. Corresponds approximately to the part-of-speech tag UH.
LST - List marker. Includes surrounding punctuation.
NAC - Not a Constituent; used to show the scope of certain prenominal modifiers within an NP.
NP - Noun Phrase. 
NX - Used within certain complex NPs to mark the head of the NP. Corresponds very roughly to N-bar level but used quite differently.
PP - Prepositional Phrase.
PRN - Parenthetical. 
PRT - Particle. Category for words that should be tagged RP. 
QP - Quantifier Phrase (i.e. complex measure/amount phrase); used within NP.
RRC - Reduced Relative Clause. 
UCP - Unlike Coordinated Phrase. 
VP - Vereb Phrase. 

WHADJP - Wh-adjective Phrase. Adjectival phrase containing a wh-adverb, as in how hot.
WHAVP - Wh-adverb Phrase. Introduces a clause with an NP gap. May be null (containing the 0 complementizer) or lexical, containing a wh-adverb such as how or why.
WHNP - Wh-noun Phrase. Introduces a clause with an NP gap. May be null (containing the 0 complementizer) or lexical, containing some wh-word, e.g. who, which book, whose daughter, none of which, or how many leopards.
WHPP - Wh-prepositional Phrase. Prepositional phrase containing a wh-noun phrase (such as of which or by whose authority) that either introduces a PP gap or is contained by a WHNP.
X - Unknown, uncertain, or unbracketable. X is often used for bracketing typos and in bracketing the...the-constructions. Clause introduced by a (possibly empty) subordinating conjunction.
SBARQ - Direct question introduced by a wh-word or a wh-phrase. Indirect questions and relative clauses should be bracketed as SBAR, not SBARQ.
SINV - Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal.
SQ - Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ.
'''
# ADJP - Adjective Phrase.
# ADVP - Adverb Phrase.
# CONJP - Conjunction Phrase.
# FRAG - Fragment.
# INTJ - Interjection. Corresponds approximately to the part-of-speech tag UH.
# LST - List marker. Includes surrounding punctuation.
# NAC - Not a Constituent; used to show the scope of certain prenominal modifiers within an NP.
# NP - Noun Phrase. 
# NX - Used within certain complex NPs to mark the head of the NP. Corresponds very roughly to N-bar level but used quite differently.
# PP - Prepositional Phrase.
# PRN - Parenthetical. 
# PRT - Particle. Category for words that should be tagged RP. 
# QP - Quantifier Phrase (i.e. complex measure/amount phrase); used within NP.
# RRC - Reduced Relative Clause. 
# UCP - Unlike Coordinated Phrase. 
# VP - Vereb Phrase. 
# WHADJP - Wh-adjective Phrase. Adjectival phrase containing a wh-adverb, as in how hot.
# WHAVP - Wh-adverb Phrase. Introduces a clause with an NP gap. May be null (containing the 0 complementizer) or lexical, containing a wh-adverb such as how or why.
# WHNP - Wh-noun Phrase. Introduces a clause with an NP gap. May be null (containing the 0 complementizer) or lexical, containing some wh-word, e.g. who, which book, whose daughter, none of which, or how many leopards.
# WHPP - Wh-prepositional Phrase. Prepositional phrase containing a wh-noun phrase (such as of which or by whose authority) that either introduces a PP gap or is contained by a WHNP.
# X - Unknown, uncertain, or unbracketable. X is often used for bracketing typos and in bracketing the...the-constructions.
# '''

'''
each time this is asked to chunk some sentences, it should first check the cache. 
'''

class SentenceChunker():

	def __init__(self):
		self.parser = stanford.StanfordParser()
		self.cache_file = 'sentence_chunker_cache.json'
	
	def get_chunks(self, sentence):

		# Check if you have already chunked this sentence
		result = self._check_cache(sentence)
		if result:
			print("***   INFO: Sentences retrieved from cache   ***")
			return result['chunks']

		# Only attempt to chunk the sentence if it's not in the cache
		else:
			print("***   INFO: Parsing sentences. This may take some time.   ***")
			# Work out the number of parts of speech in the sentence
			no_of_pos = len(sentence.split(' '))

			# Get the parse tree
			tree = next(self.parser.raw_parse(sentence))

			# Get all the labels from the tree. You need this to comparse sentences later
			labels = [sub.label() for sub in tree.subtrees()]

			# Get all the subtrees flattened as tuples
			phrases = [(sub.flatten().label(), sub.leaves()) for sub in tree.subtrees()]

			# Convert the text ^above^ into a set of labels
			all_labels = {line.split('-')[0].strip() for line in text.split('\n')}
				
			# Filter on the set of labels
			chunks = [phrase for phrase in phrases if phrase[0] in all_labels]

			# filter out the one word phrases and the full sentence
			chunks = [chunk for chunk in chunks if len(chunk[1]) > 1 and len(chunk[1]) < no_of_pos]

			# use regex to get the original chunk from the list of leaves
			sentences = []
			for chunk in chunks:
				regex = r''
				for leaf in chunk[1]:
					regex += leaf + '\s*'

				result = re.search(regex, sentence)
				if not result:
					print("***   INFO: Regex: {} didn't match sentence {}   ***".format(regex, sentence))
				
				else:
					sentences.append(result.group())

			self._write_to_cache(sentence, sentences, labels)

			return sentences


	def get_labels(self, sentence):
		results = self._check_cache(sentence)
		if results:
			return results['labels']
		else:
			# If the chunk or sentence that is passed in is not in the cache, you will need to parse it
			# the get chunks method actually does the parsing and caching, so you can just call it 
			# (ignore the chunks that come back) and then recursively call the get labels method again
			chunks = self.get_chunks(sentence)
			return self.get_labels(sentence)

	def _check_cache(self, sentence):

		# Read from the cache file
		with open('sentence_chunker_cache.json') as data_file:
			cache = json.loads(data_file.read())

			return cache.get(sentence)


	def _write_to_cache(self, sentence, chunks, labels):
	
		# Read from the cache file
		with open('sentence_chunker_cache.json') as data_file:
			cache = json.loads(data_file.read())

			# Add the new entry to the cache
			dict = {
			'chunks': chunks,
			'labels': labels
			}
			cache[sentence] = dict

		# write to the cache file again
		with open(self.cache_file, 'w') as cache_file:
			json.dump(cache, cache_file, indent=4)



if __name__ == '__main__':
	c = SentenceChunker()
	chunks = c.get_chunks("This is just an example sentence.")
	print(chunks)
	


