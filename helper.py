# Helper functions for Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com

import re


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
def get_lines_from_raw_twitter_data(fd):
    raw = fd.read()
    line_re = re.compile(r'[0-9]+\t[0-9]+\t[^\t]+\t[0-9\-]{10} [0-9:]{8}')
    return line_re.findall(raw)

def get_locations_from_raw_data(fd):
    locations = [line.split('\t')[2].lower() for line in fd.readlines()]
    locations = [re.sub(r'\(.+\)', '', loc) for loc in locations]
    locations = [process_str(loc) for loc in locations]
    return locations

# TODO: decide if we want to replace sandwiched punc chars with space 
# (consider next_non_alpha in approx matching, e.g if original tweet had:
# 'kentuky.rules ' => 'kentukyrules' doesn't approx match 'kentucky')
def process_str(s):
    lt = len(s)
    p = ''
    for a in s:
        if a.isalpha() or a == ' ':
            p += a.lower()
    return p

