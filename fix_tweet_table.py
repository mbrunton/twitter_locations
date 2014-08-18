# Some tweet bodies have newlines in them
# this script replaces them with spaces

TWEET_IN_FILE = 'data/training_set_tweets.txt'
TWEET_OUT_FILE = 'data/training_set_tweets_no_newlines.txt'

fd_in = open(TWEET_IN_FILE, 'r')
fd_out = open(TWEET_IN_FILE, 'w')

i = 0
raw = fd_in.read()
while i < len(raw):
    
