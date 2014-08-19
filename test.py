

from data_structures import Trie
from string import ascii_lowercase

def main():
    abc = ascii_lowercase + ' '
    s = 'hello there i love my silly mummy sillybugger silly'
    trie = Trie(s, abc, True)
    ms = trie.get_matches('silly', True)
    print len(ms)
    for m in ms:
        print 'm = ' + str(m)
        print s[m:m+8]



main()
