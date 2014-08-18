# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Task: Detect probable instances of US location names within
#       a corpus of tweets
#

from data_structures import TwitterCorpus, Trie
from string import ascii_lowercase
from helper import get_locations_from_raw_data
from os.path import isfile
import pickle
import re
import sys

# TWEET_FILE = '/home/subjects/comp90049/2014-sm2/project1/tweets/training_set_tweets.txt'
# LOCATION_FILE = '/home/subjects/comp90049/2014-sm2/project1/geo.../US.txt'

TWEET_FILE = 'data/tweets100.txt'
# TWEET_FILE = 'data/training_set_tweets.txt'
LOCATION_FILE = 'data/US100.txt'
# LOCATION_FILE = 'data/US.txt'
TWITTER_PICKLE_FILE = 'pickles/corpus'
TRIE_PICKLE_FILE = 'pickles/trie'

USING_PICKLES = False
RESET_PICKLES = False

def main():
    abc = ascii_lowercase + ' '

    if USING_PICKLES:
        sys.setrecursionlimit(10000)
        if not RESET_PICKLES and isfile(TWITTER_PICKLE_FILE):
            corpus = pickle.load(open(TWITTER_PICKLE_FILE, 'r'))
        else:
            corpus = TwitterCorpus(TWEET_FILE)
            pickle.dump(corpus, open(TWITTER_PICKLE_FILE, 'w'))
        print 'finished twitter corpus'

        if not RESET_PICKLES and isfile(TRIE_PICKLE_FILE):
            trie = pickle.load(open(TRIE_PICKLE_FILE, 'r'))
        else:
            trie = Trie(corpus.monolith_tweet_str, abc)
            pickle.dump(trie, open(TRIE_PICKLE_FILE, 'w'))
        print 'finished trie'
    else:
        corpus = TwitterCorpus(TWEET_FILE)
        print 'finished twitter corpus'
        trie = Trie(corpus.monolith_tweet_str, abc)
        print 'finished trie'

    locations = get_locations_from_raw_data(open(LOCATION_FILE, 'r'))
    print 'finished locations'
    print '-----------------------------------------------------------\n'

    # print_matches(trie, 'fuck')
    # print_original_tweet_matches(corpus, trie, 'fuck')
    # print_approximate_matches(trie, 'fuck', 1)
    # print_original_tweet_approximate_matches(corpus, trie, 'fuck', 1)

    # print 'trie depth: ' + str(trie.get_depth())
    found_locs = False
    for loc in locations:
        ms = trie.get_approximate_matches(loc, 1)
        if ms:
            found_locs = True
            print 'FOUND MATCHES FOR: ' + loc
            for m in ms:
                print trie.s[m:m + 3*len(loc)]
            print
    if not found_locs:
        print 'nothing found :('


# FOR DEBUGGING
def print_matches(trie, q):
    ms = trie.get_matches(q)
    for m in ms:
        print trie.s[m:m + 3*len(q)]
    print

# FOR DEBUGGING
def print_original_tweet_matches(corpus, trie, q):
    ms = trie.get_matches(q)
    for m in ms:
        id = corpus.get_id_from_index(m)
        print 'tweet id: ' + str(id)
        orig = corpus.get_original_tweet_from_id(id)
        print 'original tweet: ' + orig
    print

# FOR DEBUGGING
def print_approximate_matches(trie, q, tol):
    ms = trie.get_approximate_matches(q, tol)
    for m in ms:
        print trie.s[m:m + 3*len(q)]
    print

# FOR DEBUGGING
def print_original_tweet_approximate_matches(corpus, trie, q, tol):
    ms = trie.get_approximate_matches(q, tol)
    for m in ms:
        id = corpus.get_id_from_index(m)
        print 'tweet id: ' + str(id)
        orig = corpus.get_original_tweet_from_id(id)
        print 'original tweet: ' + orig
    print

if __name__ == '__main__':
    main()

