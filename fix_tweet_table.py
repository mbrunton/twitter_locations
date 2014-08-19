# Some tweet bodies have newlines in them
# this script replaces them with spaces

# TWEET_IN_FILE = 'data/training_set_tweets.txt'
# TWEET_OUT_FILE = 'data/training_set_tweets_no_newlines.txt'
TWEET_IN_FILE = 'data/tweets100.txt'
TWEET_OUT_FILE = 'data/tweets100_fixed.txt'


def fix():
    fd_in = open(TWEET_IN_FILE, 'r')
    fd_out = open(TWEET_OUT_FILE, 'w')

    i = 0
    raw = fd_in.read()
    while i < len(raw):
        j = i + raw[i:].find('\n')
        if j < 0:
            j = len(raw) - 1
        while num_chars(raw[i:j], '\t') != 3:
            j += raw[j+1:].find('\n')
        new_line = raw[i:j].replace('\n', '')
        # print new_line
        fd_out.write(new_line + '\n')
        i = j+1

def num_chars(s, ch):
    return sum(1 for a in s if a == ch)

fix()

