import functools

class Trie:
    def __init__(self):
        self.children = {}
        self.end_of_sentence = False

    """
    add(word)
    Description: Adds a word as the child of the word immediately preceding it
    in some sentence of the text.
    """
    def add(self, word):
        self.children[(word + ' ')] = Trie()
    
    """
    insert(sentence)
    Description: Inserts sentences into the trie, word by word.
    """
    def insert(self, sentence):
        sentence_list = sentence.split()
        current_word = self

        for word in sentence_list:
            if (word + ' ') not in current_word.children:
                current_word.add(word)
            current_word = current_word.children[(word + ' ')]

        current_word.end_of_sentence = True

    """
    get_sentences(start_of_sentence)
    Description: Given word(s) that occur at the start of some sentence in the text,
    recursively builds a set of all sentences that begin with those word(s).
    """
    def get_sentences(self, start_of_sentence):
        sentence = set()
        if self.end_of_sentence:
            sentence.add(start_of_sentence[:len(start_of_sentence) - 1] + '.')
        if not self.children:
            return sentence

        return functools.reduce(lambda a, b: a | b, [next_word.get_sentences(start_of_sentence + word) for (word, next_word) in self.children.items()]) | sentence

    """
    get_autocomplete_sentence_helper(start_of_sentence)
    Description: Given word(s) that occur at the start of some sentence in the text,
    retrieves a list of all sentences that begin with those word(s).
    """
    def get_autocomplete_sentence_helper(self, start_of_sentence):
        sentence_list = start_of_sentence.split()
        current_word = self

        for word in sentence_list:
            if (word + ' ') not in current_word.children:
                return set()
            current_word = current_word.children[(word + ' ')]

        return list(current_word.get_sentences(start_of_sentence + ' '))

