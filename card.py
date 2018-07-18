'''

'''


class Card():

	def __init__(self, sentence, chunk, chunk_translation, labels):
		self.sentence = sentence
		self.chunk = chunk
		self.chunk_translation = chunk_translation
		self.cloze_deletion = self._create_cloze_deletion(self.sentence, self.chunk)
		self.labels = labels

	def _create_cloze_deletion(self, sentence, chunk):
		return sentence.replace(chunk, '_' * len(chunk))

	def ask_question(self):
		spaces = ' ' * (len(self.cloze_deletion.split("_")[0].strip()) - 1)
		question = "{}\n{}<{}>".format(self.cloze_deletion, spaces, self.chunk_translation)

		return question

	def give_answer(self, answer):
		return answer.strip() == self.chunk.strip(), self.chunk.strip()
