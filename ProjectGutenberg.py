import collections
import heapq
import re
import string

class ProjectGutenberg:
	def __init__(self, book_fname, common_words_fname):
		self.book_fname = book_fname
		self.common_words_fname = common_words_fname
		self.book_parsed = ''
		self.common_words_parsed = ''
		self.chapter_numbers = [str(i) for i in range(1, 62)] # 61 chapters in the book

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
				else:
					self.book_parsed += line.replace('\n', ' ')

		# strip string of all punctuation
		exclude = set(string.punctuation)
		exclude.add('“') # double quotation symbol specific to the 'Pride-and-Prejudice.txt' file
		exclude.remove('-') # hyphenated words should remain that way
		self.book_parsed = self.book_parsed.replace('--', ' ')
		self.book_parsed = ''.join(ch for ch in self.book_parsed if ch not in exclude)

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
		freqs = collections.Counter(book_parsed.split())

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
		freqs = collections.Counter(book_parsed.split())

		# use a max heap
		heap = [(-freq, word) for word, freq in freqs.items()]
		heapq.heapify(heap)

		most_frequent_20_interesting_words = []
		while (heap and (len(most_frequent_20_interesting_words) < 20)):
			popped = heapq.heappop(heap)
			if popped[1] not in self.common_words_parsed and popped[1].lower() not in self.common_words_parsed:
				most_frequent_20_interesting_words.append([popped[1], -popped[0]])

		print('20 most frequent interesting words: ' + str(most_frequent_20_interesting_words))
		print()

	## get_20_least_frequent_words()
	## Description: Returns a list of the 20 least frequent words in the .txt file.
	## If multiple words are seen the same number of times, then the first 20
	## are chosen in lexical order. Chapter numbers are excluded from the list.
	def get_20_least_frequent_words(self):
		book_parsed = self.book_parsed
		freqs = collections.Counter(book_parsed.split())

		# use a min heap
		heap = [(freq, word) for word, freq in freqs.items()]
		heapq.heapify(heap)

		least_frequent_20_words = []
		while len(least_frequent_20_words) < 20:
			if not heap:
				break
			popped = heapq.heappop(heap)
			if popped[1] not in self.chapter_numbers:
				least_frequent_20_words.append([popped[1], popped[0]])

		print('20 least frequent words: ' + str(least_frequent_20_words))
		print()

