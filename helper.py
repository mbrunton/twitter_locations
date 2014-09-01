# Helper functions for Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com

import re
import configurations


# find nth occurence of substring sub in s
# returns -1 if aren't n occurences
def find_nth(s, sub, n):
    i = s.find(sub)
    while i >= 0 and n > 1:
        i = s.find(sub, i+len(sub))
        n -= 1
    return i

# return list of lines of tweet rows
# TODO: currently ignoring tweets with newlines in body
def get_lines_from_raw_twitter_data(tweet_file):
    fd = open(tweet_file, 'r')
    raw = fd.read()
    line_re = re.compile(r'[0-9]+\t[0-9]+\t[^\t]+\t[0-9\-]{10} [0-9:]{8}')
    return line_re.findall(raw)

def get_locations_from_raw_data(loc_file):
    fd = open(loc_file, 'r')
    locs = []
    for line in fd.readlines():
        raw_loc = line.split('\t')[2]
        locs.append(process_loc(raw_loc))
    return locs

# remove anything in location name that isn't strictly part of it i.e '(historical)'
def process_loc(loc):
    new_loc = re.sub(r'\(.+\)', '', loc)
    new_loc = reduce_str(new_loc)
    return new_loc

# Convert all uppercase to lowercase and just use a,b..z and space
def reduce_str(s):
    lt = len(s)
    p = ''
    for a in s:
        if a.isalpha() or a == ' ':
            p += a.lower()
    return p

