

'''
This script is just for testing. Pick random card, find the best match and
then keep going on enter
'''

from language_app import prepare_cards, select_next_question, print_parse_tree
from random import randint
cards = prepare_cards()


while True:
	print("\033[H\033[J")
	rand_int = randint(0, len(cards))
	card = cards[rand_int]
	print("Random card:")
	print('\tsentence:', card.sentence)
	print('\tchunk:', card.chunk)
	next_card = select_next_question(card, cards)[0]
	print("The best match:")
	print("\tsentence:", next_card.sentence)
	print("\tchunk:", next_card.chunk)

	print_parse_tree(card.chunk)
	print_parse_tree(next_card.chunk)
	input("Enter to continue...")



