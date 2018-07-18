'''
--- This is the first version of the language app ---

At the moment, it can:
	create a list of sentences from a text
	break each sentence into chunks
	get the translation for each chunk
'''

from read_in import SentenceReader
from cloze_deletion import SentenceChunker
from google_translate.google_translate import Translator
from parser import Comparer
from card import Card 
import re
from random import shuffle

from nltk.parse import stanford



# Loop each of the texts and create one list of all the sentences
paths = ['./input_a.txt', './input_b.txt', './input_c.txt', './input_d.txt']
sr = SentenceReader()
sentences = []
for path in paths:
	sentences.extend([sentence for sentence in sr.get_sentences(path)])

# Creates a list called sents with chunks. Each item in this list will be a list
# containing the sentence itself and another list of all the chunks for that sentence
chunker = SentenceChunker()
sents_with_chunks = []
for sentence in sentences:
	sents_with_chunks.append([sentence, chunker.get_chunks(sentence)])

# Make a list of cards
translator = Translator()
cards = []
for sent in sents_with_chunks:
	whole_sentence = sent[0]
	# Here we iterate over the chunks for each sentence and create a card for each. 
	for chunk in sent[1]:
		# check if suitable
		chunk_length = len(chunk.split(' '))
		if chunk_length >= 4 and chunk_length <= 8:
			cards.append(Card(whole_sentence, chunk, translator.get_translation(chunk), chunker.get_labels(chunk)))



# Shuffle the cards 
shuffle(cards)

# print("!!!!!!!!!!!!!!")
# print(sents_with_chunks[0])

def select_next_question(card, cards):
	'''
	This takes a card and a list of cards
	'''
	comp = Comparer()
	labels = card.labels

	# Get all cards, excluding the one that the user has just seen. 
	other_cards = [c for c in cards if c.sentence != card.sentence]

	results = []
	# iterate over all other cards 
	for other_card in other_cards:
		results.append((other_card, comp.compare(labels, other_card.labels)))

	# Get the card that is most similar
	next_card = sorted(results, key=lambda item: item[1])[0]
	print(next_card[1])
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

# card = cards[0]
# while cards:
# 	print("\033[H\033[J")
# 	print(card.ask_question())
# 	user_answer = input("Answer: ")
# 	answer = card.give_answer(user_answer)
# 	print(repr(answer))
# 	if answer[0]:
# 		# They got the question right, just pick another question
# 		shuffle(cards)
# 		card = cards.pop()
# 	else:
# 		# They got the answer wrong
# 		card, cards = select_next_question(card, cards)

# 	input('Enter to continue')




'''
just for testing, get a card, show the chunk, find the card with the best match 
'''

card = cards[0]
print("Random card:")
print('\tsentence:', card.sentence)
print('\tchunk:', card.chunk)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
next_card = select_next_question(card, cards)[0]
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("The best match:")
print("\tsentence:", next_card.sentence)
print("\tchunk:", next_card.chunk)

print_parse_tree(card.chunk)
print_parse_tree(next_card.chunk)



