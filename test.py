

from data_structures import Trie
from string import ascii_lowercase

def main():
    s = 'hello there i love my silly mummy sillybugger silly'
    abc = ''.join(set(s))
    trie = Trie(s, abc, True)
    ms = trie.get_matches_within_dist('silly', 1, True)
    print len(ms)
    for m in ms:
        print 'm = ' + str(m)
        print s[m:m+8]



main()
