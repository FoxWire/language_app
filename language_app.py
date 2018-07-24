'''
--- This is the first version of the language app ---

At the moment, it can:
	create a list of sentences from a text
	break each sentence into chunks
	get the translation for each chunk
'''

from sentence_reader import SentenceReader
from parser import Parser
from google_translate.google_translate import Translator
from comparer import TreeComparer
from card import Card 
import re
from random import shuffle
from tqdm import tqdm
from nltk.parse import stanford
import os


def prepare_cards():

	path_to_texts = './input_texts/'
	# Loop each of the texts and create one list of all the sentences
	sr = SentenceReader()
	sentences = []
	for path in os.listdir(path_to_texts):
		sentences.extend([sentence for sentence in sr.get_sentences(path_to_texts + path)])

	# For each of the sentences, create a list of parsed objects. These are just tuples with, 
	# the sentence, the list of chunks and the parse tree as a string
	parser = Parser()
	parsed_objects = [parser.parse(sentence) for sentence in tqdm(sentences)]


	'''
	Iterate over the list of parsed objects. You need to create a card for each chunk, with the 
	sentence and the parse tree for the chunk. 
	'''

	# Make a list of cards
	translator = Translator()
	cards = []
	for par_obj in tqdm(parsed_objects):
		# Here we iterate over the chunks for each sentence and create a card for each. 
		whole_sentence = par_obj[0]
		for chunk in par_obj[1]:
			# check if suitable
			chunk_length = len(chunk.split(' '))
			if chunk_length >= 4 and chunk_length <= 8:
				chunk_tree = parser.parse(chunk)[2]
				chunk_translation = translator.get_translation(chunk)
				cards.append(Card(	whole_sentence,
				 					chunk,
				 					chunk_translation,
				 					chunk_tree
				 					))

	# Shuffle the cards 
	# shuffle(cards)
	return cards


def select_next_question(card, cards):
	'''
	This takes a card and a list of cards
	'''
	comp = TreeComparer()
	# labels = card.labels

	# Get all cards, excluding the one that the user has just seen. 
	other_cards = [c for c in cards if c.sentence != card.sentence]

	results = []
	# iterate over all other cards getting their comparison score
	for other_card in tqdm(other_cards):
		results.append((other_card, comp.compare(card, other_card)))

	# Get the card that is most similar
	next_card = sorted(results, key=lambda item: item[1])[0]
	print('comparison score:', next_card[1])
	next_card = next_card[0]

	# remove the next card from the list of cards
	others = [c for c in other_cards if c != next_card]

	shuffle(others)	
	return next_card, others 

def print_parse_tree(sentence):
	'''
	This is just a test method and will be really slow if you use it in a loop
	'''
	tree = next(stanford.StanfordParser().raw_parse(sentence))
	tree.pretty_print()



'''
If they get the question right, it will just randomly select another question, if they
get it wrong, it will find the next similar one and ask it. 
Some of the stuff in the loop might not be 100% correct. 
'''


if __name__ == "__main__":
	cards = prepare_cards()
	card = cards[0]
	while cards:
		print("\033[H\033[J")
		print(card.ask_question())
		user_answer = input("Answer: ")
		answer = card.give_answer(user_answer)
		print(repr(answer))
		if answer[0]:
			# They got the question right, just pick another question
			shuffle(cards)
			card = cards.pop()
		else:
			# They got the answer wrong
			card, cards = select_next_question(card, cards)

		input('Enter to continue')	