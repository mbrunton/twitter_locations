# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Configurable settings

# files containing raw tweets
tweet_files = ['/home/subjects/comp90049/2014-sm2/project1/tweets/training_set_tweets.txt',
        'data/training_set_tweets.txt', 
        'data/tweets100.txt', 
        'data/tweets1000.txt', 
        'data/tweets10000.txt',
        'data/tweets100000.txt',
        'data/tweets1mil.txt']

class TweetFile():
    UNIMELB_SERVER, ENTIRE, HUND, THOU, TEN_THOU, HUND_THOU, MIL\
            = range(len(tweet_files))

# files containing raw US location data
loc_files = ['/home/subjects/comp90049/2014-sm2/project1/geonames/US.txt',
        'data/US1000.txt',
        'data/US10000.txt',
        'data/US100000.txt',
        'data/US.txt']

class LocFile():
    UNIMELB_SERVER, THOU, TEN_THOU, HUND_THOU, ENTIRE\
            = range(len(loc_files))

# file containing twitter user ids and location
USER_FILE = 'data/training_set_users.txt'

# pickling
USING_PICKLES = False
TWITTER_PICKLE_FILE = 'pickles/corpus'
TRIE_PICKLE_FILE = 'pickles/trie'

# do we only want substrings in our trie which start with a new word
NEW_WORD_SUBSTRINGS = True
