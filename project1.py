# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Task: Detect probable instances of US location names within
#       a corpus of tweets
#

from data_structures import TwitterCorpus, Trie
from string import ascii_lowercase

# TWEET_FILE = '/home/subjects/comp90049/2014-sm2/project1/tweets/training_set_tweets.txt'
TWEET_FILE = 


def main():
    abc = ascii_lowercase + ' '
    corpus = TwitterCorpus(TWEET_FILE)
    trie = Trie(corpus.monolith_tweet_str, abc)


main()

