import collections
import heapq
import random
import re
import string

class ProjectGutenberg:
	def __init__(self, book_fname, common_words_fname):
		self.book_fname = book_fname
		self.common_words_fname = common_words_fname
		self.book_parsed = ''
		self.book_parsed_with_punctuation = ''
		self.common_words_parsed = ''
		self.chapters = 1
		self.chapter_numbers_list = []

	## parse_book_txt_file()
	## Description: Parses the book's .txt file into a string, excluding
	## the Project Gutenberg front-matter and back-matter sections. 
	def parse_book_txt_file(self):
		with open(self.book_fname, 'r') as f:
			# start reading at 'Chapter 1\n'
			line = f.readline()
			while (line != 'Chapter 1\n'):
				line = f.readline()

			# stop reading immediately before 'End of the Project Gutenberg EBook'
			for line in f:
				if 'End of the Project Gutenberg EBook' in line:
					break

				if 'Chapter ' in line:
					self.chapters += 1

				self.book_parsed += line.replace('\n', ' ')

		self.book_parsed_with_punctuation = self.book_parsed

		# strip string of all punctuation
		exclude = set(string.punctuation)
		exclude.add('“') # double quotation symbols specific to the 'Pride-and-Prejudice.txt' file
		exclude.add('”')
		exclude.remove('-') # hyphenated words should remain that way
		self.book_parsed = self.book_parsed.replace('--', ' ')
		self.book_parsed = ''.join(ch for ch in self.book_parsed if ch not in exclude)

		self.chapter_numbers_list = [str(i) for i in range(1, self.chapters)]

	## parse_common_words_txt_file(n)
	## Description: Parses a .txt file of the 1,000 most common English words
	## into a list containing the first n words.
	## Credit for '1-1000.txt', which contains a list of the 1,000 most common
	## English words, goes to https://gist.github.com/deekayen.
	def parse_common_words_txt_file(self, n):
		if not(n >= 0 and n <= 1000):
			print('Error: The number of common words to be parsed must be between 0 and 1000 inclusive.')
			print()
			return

		with open(self.common_words_fname, 'r') as f:
			self.common_words_parsed = [next(f).replace('\n', '') for i in range(n)]

	## get_total_number_of_words()
	## Description: Returns the number of words in a .txt file using
	## regular expressions, which handles cases of punctuation marks or
	## special characters in the string.
	def get_total_number_of_words(self):
		total_number_of_words = len(re.findall(r'\w+', self.book_parsed))
		print('Total number of words: ' + str(total_number_of_words))
		print()

	## get_total_unique_words()
	## Description: Returns the number of unique words in the .txt file.
	def get_total_unique_words(self):
		book_parsed_lower = self.book_parsed.lower()
		print('Total number of unique words: ' + str(len(set(book_parsed_lower.split()))))
		print()

	## get_20_most_frequent_words()
	## Description: Returns a list of the 20 most frequent words in the .txt file,
	## including the number of times each word was used.
	def get_20_most_frequent_words(self):
		book_parsed = self.book_parsed
		freqs = dict(collections.Counter(book_parsed.split()))

		# adjust count for common nouns that are occasionally capitalized
		# at the beginning of sentences and counted as 2 distinct words
		# for example: 'the' and 'The' should be recombined as 1 entry 'the'
		# in freqs
		for word in list(freqs):
			if word[0].islower():
				capitalized_word = word[0].upper() + word[1:]
			else:
				capitalized_word = word
				word = word[0].lower() + word[1:]

			if word in freqs and capitalized_word in freqs: # not a proper noun
				freqs[word] += freqs.pop(capitalized_word)

		# adjust count for words that appear in all caps, as necessary
		for word in list(freqs):
			if len(word) == 1:
				continue

			all_caps = True
			for c in word:
				if c.islower():
					all_caps = False

			if all_caps:
				all_lower_word = ''
				for c in word:
					all_lower_word += c.lower()
				capitalized_word = all_lower_word[0].upper() + all_lower_word[1:]

				# proper noun, since double-counted common nouns were already deleted
				if capitalized_word in freqs:
					freqs[capitalized_word] += freqs.pop(word)
				elif all_lower_word in freqs: # not a proper noun
					freqs[all_lower_word] += freqs.pop(word)

		# use a max heap
		heap = [(-freq, word) for word, freq in freqs.items()]
		heapq.heapify(heap)

		most_frequent_20_words = []
		for i in range(20):
			if not heap:
				break
			popped = heapq.heappop(heap)
			most_frequent_20_words.append([popped[1], -popped[0]])

		print('20 most frequent words: ' + str(most_frequent_20_words))
		print()

	## get_20_most_interesting_frequent_words()
	## Description: Returns a list of the 20 most frequent words in the .txt file
	## after filtering out the n most common English words, where n is a
	## parameter of the method parse_common_words_txt_file(n).
	## Credit for '1-1000.txt', which contains a list of the 1,000 most common
	## English words, goes to https://gist.github.com/deekayen.
	def get_20_most_interesting_frequent_words(self):
		book_parsed = self.book_parsed
		freqs = dict(collections.Counter(book_parsed.split()))

		# adjust count for common nouns that are occasionally capitalized
		# at the beginning of sentences and counted as 2 distinct words
		# for example: 'the' and 'The' should be recombined as 1 entry 'the'
		# in freqs
		for word in list(freqs):
			if word[0].islower():
				capitalized_word = word[0].upper() + word[1:]
			else:
				capitalized_word = word
				word = word[0].lower() + word[1:]

			if word in freqs and capitalized_word in freqs: # not a proper noun
				freqs[word] += freqs.pop(capitalized_word)

		# adjust count for words that appear in all caps, as necessary
		for word in list(freqs):
			if len(word) == 1:
				continue

			all_caps = True
			for c in word:
				if c.islower():
					all_caps = False

			if all_caps:
				all_lower_word = ''
				for c in word:
					all_lower_word += c.lower()
				capitalized_word = all_lower_word[0].upper() + all_lower_word[1:]

				# proper noun, since double-counted common nouns were already deleted
				if capitalized_word in freqs:
					freqs[capitalized_word] += freqs.pop(word)
				elif all_lower_word in freqs: # not a proper noun
					freqs[all_lower_word] += freqs.pop(word)

		# use a max heap
		heap = [(-freq, word) for word, freq in freqs.items()]
		heapq.heapify(heap)

		most_frequent_20_interesting_words = []
		while (heap and (len(most_frequent_20_interesting_words) < 20)):
			popped = heapq.heappop(heap)
			if popped[1] not in self.common_words_parsed and popped[1].upper() not in self.common_words_parsed:
				most_frequent_20_interesting_words.append([popped[1], -popped[0]])

		print('20 most frequent interesting words: ' + str(most_frequent_20_interesting_words))
		print()

	## get_20_least_frequent_words()
	## Description: Returns a list of the 20 least frequent words in the .txt file.
	## If multiple words are seen the same number of times, then the first 20
	## are chosen in lexical order. Chapter numbers are excluded from the list.
	def get_20_least_frequent_words(self):
		book_parsed = self.book_parsed
		freqs = dict(collections.Counter(book_parsed.split()))

		# adjust count for common nouns that are occasionally capitalized
		# at the beginning of sentences and counted as 2 distinct words
		# for example: 'the' and 'The' should be recombined as 1 entry 'the'
		# in freqs
		for word in list(freqs):
			if word[0].islower():
				capitalized_word = word[0].upper() + word[1:]
			else:
				capitalized_word = word
				word = word[0].lower() + word[1:]

			if word in freqs and capitalized_word in freqs: # not a proper noun
				freqs[word] += freqs.pop(capitalized_word)

		# adjust count for words that appear in all caps, as necessary
		for word in list(freqs):
			if len(word) == 1:
				continue

			all_caps = True
			for c in word:
				if c.islower():
					all_caps = False

			if all_caps:
				all_lower_word = ''
				for c in word:
					all_lower_word += c.lower()
				capitalized_word = all_lower_word[0].upper() + all_lower_word[1:]

				# proper noun, since double-counted common nouns were already deleted
				if capitalized_word in freqs:
					freqs[capitalized_word] += freqs.pop(word)
				elif all_lower_word in freqs: # not a proper noun
					freqs[all_lower_word] += freqs.pop(word)

		# use a min heap
		heap = [(freq, word) for word, freq in freqs.items()]
		heapq.heapify(heap)

		least_frequent_20_words = []
		while len(least_frequent_20_words) < 20:
			if not heap:
				break
			popped = heapq.heappop(heap)
			if popped[1] not in self.chapter_numbers_list:
				least_frequent_20_words.append([popped[1], popped[0]])

		print('20 least frequent words: ' + str(least_frequent_20_words))
		print()

	## get_frequency_of_word(word)
	## Description: Returns a list of the number of times a word was used
	## in each chapter (61 chapters for Pride and Prejudice).
	## Capitalization-sensitive (ie 'the' is counted separate from 'The').
	def get_frequency_of_word(self, word):
		chapter_frequency_of_word = []
		for i in range(1, self.chapters + 1):
			chapter_start = 'Chapter ' + str(i)
			if i == self.chapters:
				chapter_stop = 'End of the Project Gutenberg EBook'
			else:
				chapter_stop = 'Chapter ' + str(i + 1)

			chapter_start_index = self.book_parsed.find(chapter_start)
			chapter_stop_index = self.book_parsed.find(chapter_stop)

			chapter_parsed = self.book_parsed[chapter_start_index:chapter_stop_index]
			chapter_parsed_list = chapter_parsed.split()
			chapter_frequency_of_word.append(chapter_parsed_list.count(word))

		print('Frequency of the word ' + '"' + word + '": ' + str(chapter_frequency_of_word))
		print()

	## get_chapter_quote_appears(quote)
	## Description: Returns the chapter in which the quote appears.
	## Capitalization-sensitive.
	def get_chapter_quote_appears(self, quote):
		for i in range(1, self.chapters + 1):
			chapter_start = 'Chapter ' + str(i)
			chapter_start_index = self.book_parsed_with_punctuation.find(chapter_start)

			if i == self.chapters: # last chapter
				chapter_parsed = self.book_parsed_with_punctuation[chapter_start_index:]
			else:
				chapter_stop = 'Chapter ' + str(i + 1)
				chapter_stop_index = self.book_parsed_with_punctuation.find(chapter_stop)
				chapter_parsed = self.book_parsed_with_punctuation[chapter_start_index:chapter_stop_index]

			if quote in chapter_parsed:
				print('Quote ' + '"' + quote + '" appears in: Chapter ' + str(i))
				print()
				return

		# once returns are implemented, should return -1 if not found
		print('Error: Quote ' + '"' + quote + '" cannot be found.')
		print()

	## generate_sentence()
	## Description: Generates a 20-word sentence in the author's style, word by word.
	## All sentences generated start with 'The'.
	def generate_sentence(self):
		sentence_list = ['The']

		while len(sentence_list) < 20:
			sentence_list.append(self.generate_next_word(sentence_list[-1]))

		punctuation = set(string.punctuation)
		punctuation.add('“') # double quotation symbols specific to the 'Pride-and-Prejudice.txt' file
		punctuation.add('”')

		# delete punctuation located at last index of the sentence
		sentence = ' '.join(sentence_list)
		if sentence[-1] in punctuation:
			sentence = sentence[:len(sentence) - 1]
		sentence += '.'

		print('Generated sentence: ' + sentence)

	## generate_next_word()
	## Description: Searches for words that the author uses immediately after
	## all instances of the word passed in. Randomly selects and returns
	## 1 of these words. More frequent words will be selected more often.
	## Capitalization-sensitive. Includes punctuation.
	def generate_next_word(self, word):
		book_parsed_list = self.book_parsed_with_punctuation.split()
		next_words = []

		done = False
		while not done:
			try:
				word_index = book_parsed_list.index(word)
				if word_index < len(book_parsed_list) - 1:
					next_words.append(book_parsed_list[word_index + 1])
					book_parsed_list = book_parsed_list[word_index + 1:]
			except ValueError: # not found
				done = True

		random_index = random.randint(0, len(next_words) - 1)
		return next_words[random_index]





























