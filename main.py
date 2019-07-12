from ProjectGutenberg import *

## Credit for 'Pride-and-Prejudice.txt' goes to Project Gutenberg.
def main():
	p_and_p = ProjectGutenberg('Pride-and-Prejudice.txt', '1-1000.txt')
	p_and_p.parse_book_txt_file()
	
	p_and_p.get_total_number_of_words()
	p_and_p.get_total_unique_words()
	p_and_p.get_20_most_frequent_words()

	# filters out the 300 most common English words
	p_and_p.parse_common_words_txt_file(300)
	p_and_p.get_20_most_interesting_frequent_words()

	p_and_p.get_20_least_frequent_words()

main()

