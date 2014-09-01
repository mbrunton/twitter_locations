# Data Structures for use in Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Post processing of matches

from data_structures import TwitterCorpus
from configurations import *
import nltk
import sys

# Generate list of most common words found in a sample of tweets
def generate_stopwords(tweet_str, per=0.3):
    words = tweet_str.split()
    fd = nltk.FreqDist(words)
    items = fd.items()
    stopwords = []
    total_words = sum(fd.values())
    count = 0
    while float(count) / total_words < per:
        word = items[0][0]
        freq = items[0][1]
        stopwords.append(word)
        count += freq
        items = items[1:]
    return stopwords

def intersect(list1, list2):
    return [x for x in list1 if x in list2]

def remove_stopwords(loc_matches, stopwords):
    pruned_loc_matches = []
    for (loc, ms) in loc_matches:
        pruned_ms = [m for m in ms if m.string not in stopwords]
        pruned_loc_matches.append( (loc[:], pruned_ms) )
    return pruned_loc_matches

def get_accuracy(loc_matches):
    count = 0.
    for (loc, ms) in loc_matches:
        for m in ms:
            if m.loc == m.true_loc:
                count += 1.
    num_matches = sum(len(ms) for (loc, ms) in loc_matches)
    if num_matches == 0:
        return 0.
    return count / num_matches

def main():
    argv = sys.argv
    if len(argv) != 3:
        print 'usage: python ' + argv[0] + ' ',
        print '<tweet file> <percentage>'
        exit()
    tweet_file = argv[1]
    per = float(argv[2])
    corpus = TwitterCorpus(tweet_file, USER_FILE)
    stopwords = generate_stopwords(corpus.monolith_tweet_str,per=per)
    print stopwords

if __name__ == '__main__':
    main()
