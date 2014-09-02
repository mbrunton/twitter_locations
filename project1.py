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
from helper import *
from post_processing import *
from configurations import *
from string import ascii_lowercase
from os.path import isfile
import cPickle
import re
import sys
from marisa_trie import Trie as MarisaTrie


def main():
    sys.setrecursionlimit(1000000)
    abc = ascii_lowercase + ' '

    argv = sys.argv
    if len(argv) != 3 and len(argv) != 4:
        print 'usage: python ' + argv[0] + ' ',
        print '<tweet file> <location file> ',
        print '(optional) <output file>'
        exit()
    tweet_file = argv[1]
    loc_file = argv[2]
    if len(argv) == 4:
        out_file = argv[3]
    else:
        out_file = None

    corpus = TwitterCorpus(tweet_file, USER_FILE)
    print 'finished twitter corpus'
    trie = Trie(corpus.monolith_tweet_str, abc, new_word_substrings=NEW_WORD_SUBSTRINGS)
    print 'finished trie'

    locations = get_locations_from_parsed_data(loc_file)
    print 'finished locations'
    print '-----------------------------------------------------------\n'

    print 'number of locations: ' + str(len(locations))
    print 'number of tweets: ' + str(corpus.get_num_tweets())
    i = 0
    loc_matches = []
    for loc in locations:
        #print 'matches for ' + loc + '...'
        dist = min(int(DIST_PER_LENGTH * len(loc)), MAX_DIST)
        ms = trie.get_matches_within_dist(loc, dist, ends_in_space=True)
        for m in ms:
            m.set_string(corpus.monolith_tweet_str[m.index: m.index+m.length])
            id = corpus.get_id_from_index(m.index)
            m.set_tweet_id(id)
            m.set_loc(loc)
            m.set_true_loc(corpus.get_location_from_id(id))
            #print m.string + ' matches ' + m.loc
            #tweet = corpus.get_tweet_from_id(id)
            #print tweet
        loc_matches.append( (loc, ms) )
        i += 1
        #print 'number of locations processed: ' + str(i)
    print 'finished finding matches'

    # determining best stopword percentage
    per = 0.7
    stopwords = generate_stopwords(corpus.monolith_tweet_str, per=per)
    #loc_matches = remove_stopwords(loc_matches, stopwords)
    print 'after pruning...'
    for (loc, ms) in loc_matches:
        for m in ms:
            if 'sin' == m.string.strip():
                tweet = corpus.get_tweet_from_id(m.tweet_id)
                print tweet
                print
    accuracy = get_accuracy(loc_matches)
    print 'accuracy: ' + str(accuracy * 100) + '%'

    if out_file:
        out_fd = open(out_file, 'w')
        for (loc, ms) in loc_matches:
            out_fd.write(loc + '\n')
            for m in ms:
                out_fd.write(str(m.index) + '\n')
        out_fd.close()


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



