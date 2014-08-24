# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Task: Detect probable instances of US location names within
#       a corpus of tweets
#
# Note: To reset pickless, add the parameter '--reset-pickles' when
#       the program is run


from data_structures import TwitterCorpus, Trie
from distance import MetricType
from helper import get_locations_from_raw_data
from configurations import *

from string import ascii_lowercase
from os.path import isfile
import cPickle
import re
import sys


def main():
    abc = ascii_lowercase + ' '

    if USING_PICKLES:
        sys.setrecursionlimit(10000)
        argv = sys.argv
        reset = argv and (argv[0] == '--reset-pickes')

        if not reset and isfile(TWITTER_PICKLE_FILE):
            corpus = cPickle.load(open(TWITTER_PICKLE_FILE, 'r'))
        else:
            corpus = TwitterCorpus(TWEET_FILE)
            cPickle.dump(corpus, open(TWITTER_PICKLE_FILE, 'w'))
        print 'finished twitter corpus'

        if not reset and isfile(TRIE_PICKLE_FILE):
            trie = cPickle.load(open(TRIE_PICKLE_FILE, 'r'))
        else:
            trie = Trie(corpus.monolith_tweet_str, abc, new_word_substrings=NEW_WORD_SUBSTRINGS)
            cPickle.dump(trie, open(TRIE_PICKLE_FILE, 'w'))
        print 'finished trie'
    else:
        corpus = TwitterCorpus(TWEET_FILE)
        print 'finished twitter corpus'
        trie = Trie(corpus.monolith_tweet_str, abc, new_word_substrings=NEW_WORD_SUBSTRINGS)
        print 'finished trie'

    locations = get_locations_from_raw_data(open(LOCATION_FILE, 'r'))
    print 'finished locations'
    print '-----------------------------------------------------------\n'

    # print_matches(trie, 'fuck')
    # print_original_tweet_matches(corpus, trie, 'fuck')
    # print 'trie depth: ' + str(trie.get_depth())

    for loc in locations:
        ms = trie.get_matches_within_dist(loc, 0, ends_in_space=True)
        #ms = trie.get_matches(loc, ends_in_space=False)
        if ms:
            found_locs = True
            print 'FOUND MATCHES FOR: ' + loc
            for m in ms:
                print trie.s[m:m + 3*len(loc)]
            print

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


if __name__ == '__main__':
    main()



