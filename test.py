

from data_structures import Trie
from string import ascii_lowercase

def main():
    s = 'abaca abada baca abac abacd abaca'
    abc = ''.join(set(s))
    trie = Trie(s, abc, True)
    ms = trie.get_matches_within_dist('abaca', 1, False)
    print len(ms)
    for m in ms:
        print 'm = ' + str(m)
        print s[m:m+8]



main()
