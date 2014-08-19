# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Module containing different notions of 'distance'
# when comparing the closeness of two strings

from string import ascii_lowercase


class MetricType():
	EDIT_DIST, EDITEX, SOUNDEX  = range(3)
	

# EDIT DISTANCE
# returns the standard edit distance between two strings
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

# c1, c2 are letters
def equal(c1, c2):
    if c1 == c2:
        return 0
    return 1
	
# EDITEX
# returns the edit distance between two strings' editex code
def editex_dist(s, t, letter_groups):
	if not s:
		return len(t)
	if not t:
		return len(s)
	s = ' ' + s
	t = ' ' + t
	ls = len(s)
	lt = len(t)
	dists = [[0 for j in range(lt)] for i in range(ls)]
	for i in range(ls):
		dists[i][0] = i
	for j in range(lt):
		dists[0][j] = j
	for i in range(1, ls):
		for j in range(1, lt):
			d1 = dists[i-1][j] + 1
			d2 = dists[i][j-1] + 1
			d3 = dists[i-1][j-1] + editex_equal(s[i], t[j])
			dists[i][j] = min(d1, d2, d3)
	s = s[1:]
	t = t[1:]
	return dists[-1][-1]

# check if c1, c2 occur in the same group anywhere
def editex_equal(c1, c2, letter_groups):
	v1 = [group for group in letter_groups if c1 in group]
	v2 = [group for group in letter_groups if c2 in group]
	intersect = [group for group in v1 if group in v2]
	if intersect:
		return 0
	return diff(c1, c2)
	
# TODO: check groupings against slides
def get_editex_groups():
    letter_groups = [['a', 'e', 'i', 'o', 'u', 'y', 'w', 'h'], 
                     ['b', 'p'], ['f', 'p', 'v'], ['m', 'n'], 
                     ['c', 'k', 'q'], ['s', 'x', 'z'], ['c', 's', 'z'],
                     ['r', 'l'], ['d', 't'], ['g', 'j']]
    return letter_groups

	
# SOUNDEX
# returns true for same soundex value
def soundex(s, t, d):
	sx = get_soundex_code(s, d)
	tx = get_soundex_code(t, d)
	return sx == tx
	
def get_soundex_dict():
    abc = ascii_lowercase + ' '
    d = {}
    for c in abc:
        if c in 'aeiouhwy':
            d[c] = '0'
        elif c in 'bfpv':
            d[c] = '1'
        elif c in 'cgjkqsxz':
            d[c] = '2'
        elif c in 'dt':
            d[c] = '3'
        elif c in 'mn':
            d[c] = '5'

    d['l'] = '4'
    d['r'] = '6'
    d[' '] = ''
    return d


def get_soundex_code(s, d):
    if not s:
        return ''
    code = s[0]
    for c in s[1:]:
        code += d[c]
    code = code[0] + ''.join(code[i] for i in range(1, len(code)) if code[i] != code[i-1])
    code = ''.join(c for c in code if c != '0')
    code = code[:4]
    return code



