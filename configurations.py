# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Configurable settings


# file containing raw tweets
# TWEET_FILE = '/home/subjects/comp90049/2014-sm2/project1/tweets/training_set_tweets.txt'
# TWEET_FILE = 'data/tweets1mil.txt'
# TWEET_FILE = 'data/training_set_tweets.txt'
TWEET_FILE = 'data/tweets1000.txt'

# file containing raw US location data
# LOCATION_FILE = '/home/subjects/comp90049/2014-sm2/project1/geo.../US.txt'
# LOCATION_FILE = 'data/US1000.txt'
LOCATION_FILE = 'data/US.txt'

TWITTER_PICKLE_FILE = 'pickles/corpus'
TRIE_PICKLE_FILE = 'pickles/trie'

USING_PICKLES = False

# do we only want substrings in our trie which start with a new word
NEW_WORD_SUBSTRINGS = True
