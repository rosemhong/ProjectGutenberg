from project_gutenberg import *

"""
display_menu()
Description: Displays a list of options to the user.
"""
def display_menu(book_fname):
	print()
	print('What would you like to do with the text ' + '"' + book_fname + '"?')
	print('1. Get the total number of chapters.')
	print('2. Get the total number of words.')
	print('3. Get the total number of unique words.')
	print('4. Get the 20 most frequently-occuring words.')
	print('5. Get the 20 most frequently-occuring words, excluding the 300 most common English words.')
	print('6. Get the 20 least frequently-occuring words.')
	print('7. Get the frequency of a word by chapter.')
	print('8. Get the chapter in which a quote appears.')
	print("9. Generate a 20-word sentence in the author's style.")
	print('10. Autocomplete a sentence.')

"""
menu()
Description: Displays a list of options to the user and performs functions
based on the user's input.
"""
def menu(book, book_fname):
	quit = ['Q', 'q', 'Quit', 'quit']
	no = ['N', 'n', 'No', 'no']

	display_menu(book_fname)
	option = input('\nEnter an option between 1 and 10 inclusive, or Q to quit: ')
	while option not in quit:
		if option.isalpha() and option not in quit:
			print('\nError: Option invalid.')
		elif option.isnumeric() and (int(option) < 1 or int(option) > 10):
			print('\nError: Option invalid.')
		else:
			if option == '1':
				print('\nTotal number of chapters: ' + str(book.get_total_number_of_chapters()))
			elif option == '2':
				print('\nTotal number of words: ' + str(book.get_total_number_of_words()))
			elif option == '3':
				print('\nTotal number of unique words: ' + str(book.get_total_unique_words()))
			elif option == '4':
				print('\n20 most frequently-occuring words: ' + str(book.get_20_most_frequent_words()))
			elif option == '5':
				print('\n20 most frequently-occuring interesting words: ' + str(book.get_20_most_interesting_frequent_words()))
			elif option == '6':
				print('\n20 least frequently-occuring words: ' + str(book.get_20_least_frequent_words()))
			elif option == '7':
				word = input('\nWhich word would you like to get the frequency of?: ')
				print('Frequency of the word ' + '"' + word + '" by chapter: ' + str(book.get_frequency_of_word(word)))
			elif option == '8':
				quote = input('\nWhich quote would you like to get the chapter of?: ')
				chapter = book.get_chapter_quote_appears(quote)
				if chapter == -1:
					print('Error: Quote ' + '"' + quote + '" cannot be found.')
				else:
					print('Quote ' + '"' + quote + '" appears in: Chapter ' + str(chapter))
			elif option == '9':
				print('\nGenerated sentence: ' + book.generate_sentence())
			elif option == '10':
				start_of_sentence = input('\nWhich word or phrase would you like to autocomplete?: ')
				autocomplete_sentences = book.get_autocomplete_sentences(start_of_sentence)
				if not autocomplete_sentences:
					print('Error: No autocomplete sentences found.')
				else:
					print('\nAutocomplete sentences starting with ' + '"' + start_of_sentence + '":')
					for i in range(len(autocomplete_sentences)):
						print(str(i + 1) + '. ' + autocomplete_sentences[i])

		option = input('\nWould you like to choose another option? (Y/N): ')
		if option in no:
			print('\nExited Project Gutenberg Analysis Project.')
			print()
			return
		else:
			display_menu(book_fname)
			option = input('\nEnter an option between 1 and 10 inclusive, or Q to quit: ')

	if option in quit:
		print('\nExited Project Gutenberg Analysis Project.')
		print()

## Credit for 'Pride-and-Prejudice.txt' goes to Project Gutenberg.
def main():
	print()
	print('Welcome to the Project Gutenberg Analysis Project.')
	book_fname = input('\nWhich .txt file would you like to analyze? (Q to quit): ')
	found_fname = False
	while not found_fname and book_fname != 'Q' and book_fname != 'q':
		try:
			book = ProjectGutenberg(book_fname, '1-1000.txt')
			found_fname = True
			menu(book, book_fname)
		except FileNotFoundError:
			print('Error: File not found.')
			book_fname = input('\nWhich .txt file would you like to analyze? (Q to quit): ')

	if book_fname == 'Q' or book_fname == 'q':
		print('\nExited Project Gutenberg Analysis Project.')
		print()

main()