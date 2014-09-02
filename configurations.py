# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Configurable settings

# file containing twitter user ids and their locations
USER_FILE = 'data/training_set_users.txt'

# do we only want substrings in our trie which start with a new word
NEW_WORD_SUBSTRINGS = True

# how much edit dist will we allow per character
DIST_PER_LENGTH = (1.0 / 10.0)

# max edit distance
MAX_DIST = 2
