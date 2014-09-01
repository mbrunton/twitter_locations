# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Configurable settings

# file containing twitter user ids and their locations
USER_FILE = 'data/training_set_users.txt'

# pickling
USING_PICKLES = True
RESET_PICKLES = False
TWITTER_PICKLE_FILE = 'pickles/corpus'
TRIE_PICKLE_FILE = 'pickles/trie'

# do we only want substrings in our trie which start with a new word
NEW_WORD_SUBSTRINGS = True
