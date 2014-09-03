# Data Structures for use in Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Functions for post processing of matches after initial 
# approximate string match

from data_structures import TwitterCorpus
from configurations import *
import nltk
import sys

# Generate list of most common words found in a sample of tweets
def generate_stopwords(tweet_str, per=0.45):
    words = tweet_str.split()
    fd = nltk.FreqDist(words)
    items = fd.items()
    stopwords = []
    total_words = len(words)
    count = 0
    i = 0
    while i < len(items) and float(count) / total_words < per:
        word = items[i][0]
        freq = items[i][1]
        stopwords.append(word)
        count += freq
        i += 1
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

def get_max_stopword_percentage(corpus, loc_matches):
    per = 0.01
    max_acc = 0.
    while per < 1.00:
        stopwords = generate_stopwords(corpus.monolith_tweet_str, per=per)
        pruned_loc_matches = remove_stopwords(loc_matches, stopwords)
        accuracy = get_accuracy(pruned_loc_matches)
        if accuracy > max_acc:
            max_acc = accuracy
            max_per = per
        per += 0.01
    if max_per:
        return max_per
    return 0.

# this is just for testing which stopwords are produced for different
# text and per values
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
