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
    locations = [re.sub(r'[.\-\']', '', loc) for loc in locations]
    return locations

# a1, a2 are letters
def equal(a1, a2):
    if a1 == a2:
        return 0
    return 1

def edit_distance(s, t):
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)
    # from s to t
    s = ' ' + s
    t = ' ' + t
    ls = len(s)
    lt = len(t)
    dists = [[0 for j in range(lt)] for i in range(ls)]
    for j in range(lt):
        dists[0][j] = j
    for i in range(ls):
        dists[i][0] = i

    for i in range(1, ls):
        for j in range(1, lt):
            d1 = dists[i-1][j] + 1
            d2 = dists[i][j-1] + 1
            d3 = dists[i-1][j-1] + equal(s[i], t[j])
            dists[i][j] = min(d1, d2, d3)
    s = s[1:]
    t = t[1:]
    return dists[-1][-1]


# TODO: decide if we want to replace sandwiched punc chars with space 
# (consider next_non_alpha in approx matching, e.g if original tweet had:
# 'kentuky.rules ' => 'kentukyrules' doesn't approx match 'kentucky')
def process_str(s):
    lt = len(s)
    p = ''
    for a in s:
        if a.isalpha():
            p += a.lower()
        elif a.isspace():
            p += ' '
    return p

