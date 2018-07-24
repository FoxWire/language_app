'''

'''


class Card():

	def __init__(self, sentence, chunk, chunk_translation, tree_string):
		self.sentence = sentence
		self.chunk = chunk
		self.chunk_translation = chunk_translation
		self.cloze_deletion = self._create_cloze_deletion(self.sentence, self.chunk)
		self.tree_string = self._format_tree_string(tree_string)

	def _create_cloze_deletion(self, sentence, chunk):
		return sentence.replace(chunk, '_' * len(chunk))

	def ask_question(self):
		spaces = ' ' * (len(self.cloze_deletion.split("_")[0].strip()) - 1)
		question = "{}\n{}<{}>".format(self.cloze_deletion, spaces, self.chunk_translation)

		return question

	def give_answer(self, answer):
		return answer.strip() == self.chunk.strip(), self.chunk.strip()

	def _format_tree_string(self, tree_string):
		# remove the newlines and whitespace that comes with tree strings
		return "".join(tree_string.split())

	def __str__(self):
		s = "\nsentence: {}\n chunk: {}\n chunk translation: {}\n tree_string: {}\n".format(
			self.sentence, self.chunk, self.chunk_translation, self.tree_string)
		return s
