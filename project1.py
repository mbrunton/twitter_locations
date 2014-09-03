# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Task: Detect probable instances of US location names within
#       a corpus of tweets
#
# Usage: python project1.py <tweet file> <location file> (optional)<output file>


from data_structures import TwitterCorpus, Trie
from helper import *
from post_processing import *
from string import ascii_lowercase
from os.path import isfile
import cPickle
import re
import sys


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
    trie = Trie(corpus.monolith_tweet_str, abc, new_word_substrings=NEW_WORD_SUBSTRINGS)
    locations = get_locations_from_parsed_data(loc_file)

    loc_matches = []
    for loc in locations:
        dist = min(int(DIST_PER_LENGTH * len(loc)), MAX_DIST)
        ms = trie.get_matches_within_dist(loc, dist, ends_in_space=True)
        for m in ms:
            m.set_string(corpus.monolith_tweet_str[m.index: m.index+m.length].strip())
            id = corpus.get_id_from_index(m.index)
            m.set_tweet_id(id)
            m.set_loc(loc)
            m.set_true_loc(corpus.get_location_from_id(id))
        loc_matches.append( (loc, ms) )

    stopwords = generate_stopwords(corpus.monolith_tweet_str)
    loc_matches = remove_stopwords(loc_matches, stopwords)

    if out_file:
        out_fd = open(out_file, 'w')
        for (loc, ms) in loc_matches:
            out_fd.write(loc + '\n')
            for m in ms:
                out_fd.write(str(m.tweet_id) + '\n')
        out_fd.close()
    else:
        for (loc, ms) in loc_matches:
            print loc
            for m in ms:
                print m.tweet_id
    return


if __name__ == '__main__':
    main()



