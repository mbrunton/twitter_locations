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
from validate import validate_matches
from configurations import *

from string import ascii_lowercase
from os.path import isfile
import cPickle
import re
import sys


def main():
    sys.setrecursionlimit(10000)
    abc = ascii_lowercase + ' '
    tweet_file = TweetFile.HUND_THOU
    loc_file = LocFile.HUND_THOU

    if USING_PICKLES:
        argv = sys.argv
        reset = argv and (argv[0] == '--reset-pickes')
        if not reset and isfile(TWITTER_PICKLE_FILE):
            corpus = cPickle.load(open(TWITTER_PICKLE_FILE, 'r'))
        else:
            corpus = TwitterCorpus(tweet_file, USER_FILE)
            cPickle.dump(corpus, open(TWITTER_PICKLE_FILE, 'w'))
        print 'finished twitter corpus'

        if not reset and isfile(TRIE_PICKLE_FILE):
            trie = cPickle.load(open(TRIE_PICKLE_FILE, 'r'))
        else:
            trie = Trie(corpus.monolith_tweet_str, abc, new_word_substrings=NEW_WORD_SUBSTRINGS)
            cPickle.dump(trie, open(TRIE_PICKLE_FILE, 'w'))
        print 'finished trie'
    else:
        corpus = TwitterCorpus(tweet_file, USER_FILE)
        print 'finished twitter corpus'
        trie = Trie(corpus.monolith_tweet_str, abc, new_word_substrings=NEW_WORD_SUBSTRINGS)
        print 'finished trie'

    locations = get_locations_from_raw_data(loc_file)
    print 'finished locations'
    print '-----------------------------------------------------------\n'

    print 'number of locations: ' + str(len(locations))
    print 'number of tweets: ' + str(corpus.get_num_tweets())
    i = 0
    loc_matches = []
    for loc in locations:
        print 'matches for ' + loc + '...'
        ms = trie.get_matches_within_dist(loc, 1, ends_in_space=True)
        if ms:
            for m in ms:
                id = corpus.get_id_from_index(m)
                tweet = corpus.get_tweet_from_id(id)
                print tweet
            print
        loc_matches.append( (loc, ms) )
        i += 1
        print 'number of locations processed: ' + str(i)


# FOR DEBUGGING
def print_substring_matches(trie, q):
    ms = trie.get_matches(q)
    for m in ms:
        print trie.s[m:m + 3*len(q)]
    print

# FOR DEBUGGING
def print_tweet_matches(corpus, trie, q):
    ms = trie.get_matches(q)
    for m in ms:
        id = corpus.get_id_from_index(m)
        print 'tweet id: ' + str(id)
        tweet = corpus.get_tweet_from_id(id)
        print 'tweet: ' + tweet
    print


if __name__ == '__main__':
    main()



