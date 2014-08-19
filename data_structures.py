# Data Structures for use in Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com

from helper import get_lines_from_raw_twitter_data
from helper import process_str
from distance import *

class TwitterCorpus():
    def __init__(self, file):
        fd = open(file, 'r')
        id_to_tweet = {}
        index_to_id = {}

        # TODO: fix this method
        lines = get_lines_from_raw_twitter_data(fd)
        for line in lines:
            fields = line.split('\t')
            tweet_id = int(fields[1])
            tweet_text = fields[2]
            id_to_tweet[tweet_id] = tweet_text

        processed_tweets_list = []
        next_index = 0
        for item in id_to_tweet.items():
            tweet_id = item[0]
            raw_tweet = item[1]
            index_to_id[next_index] = tweet_id
            processed_tweet = process_str(raw_tweet) + ' '
            processed_tweets_list.append(processed_tweet)
            next_index += len(processed_tweet)

        self.id_to_tweet = id_to_tweet
        self.index_to_id = index_to_id
        self.processed_tweets = processed_tweets_list
        self.monolith_tweet_str = ''.join(processed_tweets_list)

    # index is within self.monolith_tweet_str
    def get_id_from_index(self, index):
        if index < 0:
            return None
        d = self.index_to_id
        while index not in d:
            index -= 1
        return d[index]

    def get_original_tweet_from_id(self, id):
        if id in self.id_to_tweet:
            return self.id_to_tweet[id]


class Trie():
    def __init__(self, s, abc, new_word_substrings=False):
        if '\0' not in abc:
            abc += '\0'
        if len(set(abc)) != len(abc):
            raise Exception('alphabet contains duplicates')
        for a in s:
            if a not in abc:
                raise Exception('alphabet does not contain char: ' + a)
        self.s = s
        self.abc = abc
        self.root = TrieNode(abc, 0)
        ls = len(s)
        one_percent = ls / 100
        percent = 0
        for i in range(ls):
            # are we using all substrings, or just those which start with beginnning of word
            if not new_word_substrings or i == 0 or (s[i-1] == ' ' and s[i].isalpha()):
                self.root.add_suffix(s, i)
            if i % one_percent == 0:
                print 'at ' + str(percent) + '%'
                percent += 1
            
    def get_matches(self, q):
        return self.root.get_matches(self.s, q)

    def get_approximate_matches(self, q, metric, tol):
        if metric == MetricType.EDITEX:
            letter_groups = get_editex_groups()
            return self.root.get_approximate_matches(self.s, q, metric, tol, letter_groups=letter_groups)
        elif metric == MetricType.SOUNDEX:
            return self.root.get_approximate_matches(self.s, q, metric, tol, soundex_dict=soundex_dict)
        return self.root.get_approximate_matches(self.s, q, metric, tol)
        
    def get_depth(self):
        return self.root.get_subtrie_depth()

class TrieNode():
    def __init__(self, abc, depth):
        self.abc = abc
        self.depth = depth
        self.bs = {} # branches
        for a in abc:
            self.bs[a] = None
            
    def add_suffix(self, s, i):
        # i is index of start of suffix in s
        if i + self.depth >= len(s):
            self.bs['\0'] = i
            return
        first = s[i + self.depth]
        if self.bs[first] == None:
            self.bs[first] = i
        elif type(self.bs[first]) == int:
            old_index = self.bs[first]
            self.bs[first] = TrieNode(self.abc, self.depth+1)
            self.bs[first].add_suffix(s, old_index)
            self.bs[first].add_suffix(s, i)
        else:
            # bs[first] is another Node
            self.bs[first].add_suffix(s, i)
            
    def get_matches(self, s, q):
        if self.depth >= len(q):
            return self.scrape_node()
        first = q[self.depth]
        if self.bs[first] == None:
            return []
        elif type(self.bs[first]) == int:
            ls = len(s)
            for i in range(len(q)):
                j = self.bs[first] + i
                if j >= ls or s[j] != q[i]:
                    return []
            return [self.bs[first]]
        else:
            return self.bs[first].get_matches(s, q)

    def get_approximate_matches(self, s, q, metric, tol, letter_groups=None, soundex_dict=None):
        if tol == 0:
            matches = self.get_matches(s, q)
            return self.prune_matches(matches, s, q, metric, tol, letter_groups, soundex_dict)
        matches = []
        try:
            first = q[self.depth]
        except IndexError:
            first = None
        for item in self.bs.items():
            k = item[0]
            v = item[1]
            if v == None:
                continue
            elif type(v) == int:
                return [self.prune_matches([v], s, q, metric, tol, letter_groups, soundex_dict)]
            else:
                # v is a another node
                child = v
                # TODO: should our equal function depend on metric type?
                tol_diff = equal(k, first)
                matches += child.get_approximate_matches(s, q, metric, tol-tol_diff)
                # TODO: consider insertion and deletion as well
                # need to have effective_level counter
        return matches

    def prune_matches(self, matches, s, q, metric, tol, letter_groups, soundex_dict):
        pruned = []
        lq = len(q)
        for m in matches:
            next_space = m + lq + s[m + lq:].find(' ')
            if next_space < 0:
                next_space = len(s)
            substring = s[m: next_space]
            if metric == MetricType.EDIT_DIST:
                dist = edit_distance(substring, q)
                if dist <= tol:
                    pruned.append(m)
            elif metric == MetricType.EDITEX:
                dist = editex(substring, q)
                if dist <= tol:
                    pruned.append(m)
            else:
                # metric == MetricType.Soundex
                same_soundex = soundex(substring, q)
                if same_soundex:
                    pruned.append(v)
        return pruned


    def scrape_node(self):
        indices = []
        for v in self.bs.values():
            if type(v) == int:
                indices.append(v)
            elif type(v) == TrieNode:
                indices += v.scrape_node()
        return indices

    def get_subtrie_depth(self):
        subnodes = [v for v in self.bs.values() if v is not None and type(v) != int]
        if not subnodes:
            return self.depth
        return max(node.get_subtrie_depth() for node in subnodes)

    # TODO
    def get_longest_repeated_substring(self):
        pass




