

from data_structures import Trie
from string import ascii_lowercase

def main():
    s = 'garfield'
    abc = ''.join(set(s))
    trie = Trie(s, abc, True)
    ms = trie.get_matches_within_dist('garfeld', 1, ends_in_space=True)
    print 'number of matches: ' + str(len(ms))
    for m in ms:
        print m.index,
        print ', ',
        print m.length


main()
