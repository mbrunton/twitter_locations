# Data Structures for use in Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com

from helper import get_lines_from_raw_twitter_data
from helper import reduce_str, process_loc
from distance import edit_dist, equal

class TwitterCorpus():
    def __init__(self, tweet_file_index, user_file):
        id_to_tweet = {}
        index_to_id = {}
        id_to_loc = {}

        user_fd = open(user_file, 'r')
        user_id_to_loc = {}
        for line in user_fd.readlines():
            fields = line.split('\t')
            user_id = int(fields[0])
            loc = process_loc(fields[1])
            user_id_to_loc[user_id] = loc

        lines = get_lines_from_raw_twitter_data(tweet_file_index)
        tweets = []
        next_index = 0
        for line in lines:
            fields = line.split('\t')
            user_id = int(fields[0])
            tweet_id = int(fields[1])
            tweet_text = reduce_str(fields[2]) + ' '
            tweets.append(tweet_text)

            id_to_tweet[tweet_id] = tweet_text
            id_to_loc[tweet_id] = user_id_to_loc[user_id]
            index_to_id[next_index] = tweet_id
            next_index += len(tweet_text)

        self.id_to_tweet = id_to_tweet
        self.index_to_id = index_to_id
        self.id_to_loc = id_to_loc
        self.monolith_tweet_str = ''.join(tweets)

    def get_id_from_index(self, index):
        start_index = self.get_tweet_start_index_from_index(index)
        return self.index_to_id[start_index]

    def get_tweet_start_index_from_index(self, index):
        if index < 0:
            return None
        d = self.index_to_id
        while index not in d:
            index -= 1
        return index

    def get_tweet_from_id(self, id):
        if id in self.id_to_tweet:
            return self.id_to_tweet[id]

    def get_location_from_id(self, id):
        if id in self.id_to_loc:
            return self.id_to_loc[id]

    def get_accuracy(self, ms, loc):
        if not ms:
            return 0.
        correct = 0.
        for m in ms:
            id = self.get_id_from_index(m)
            true_loc = self.get_location_from_id(id)
            if true_loc == loc:
                correct += 1.
        return correct / len(ms)

    def get_num_tweets(self):
        return len(self.id_to_tweet.items())


class Trie():
    def __init__(self, s, abc, new_word_substrings):
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
        for i in range(ls):
            # are we using all substrings, or just those which start a new word
            if (not new_word_substrings) or i == 0 or (s[i-1].isspace() and s[i].isalpha()):
                self.root.add_suffix(s, i, 0)

    def get_matches(self, q, ends_in_space=False):
        return self.root.get_matches(self.s, q, 0, ends_in_space)

    def get_matches_within_dist(self, q, dist, ends_in_space=False):
        ms = self.root.get_matches_within_dist(self.s, q, dist, 0, ends_in_space)
        return list(set(ms))

    def get_depth(self):
        return self.root.get_subtrie_depth(0)

class TrieNode():
    def __init__(self, abc, true_depth):
        self.abc = abc
        self.true_depth = true_depth
        self.bs = {} # branches
        for a in abc:
            self.bs[a] = None
            
    def add_suffix(self, s, i, depth):
        # i is index of start of suffix in s
        if i + depth >= len(s):
            self.bs['\0'] = i
            return
        schar = s[i + depth]
        if self.bs[schar] == None:
            self.bs[schar] = i
        elif type(self.bs[schar]) == int:
            old_index = self.bs[schar]
            self.bs[schar] = TrieNode(self.abc, self.true_depth+1)
            self.bs[schar].add_suffix(s, old_index, depth+1)
            self.bs[schar].add_suffix(s, i, depth+1)
        else:
            # bs[schar] is another Node
            self.bs[schar].add_suffix(s, i, depth+1)

    def get_matches(self, s, q, depth, ends_in_space):
        if depth == len(q):
            return self.scrape_node(ends_in_space)
        qchar = q[depth]
        if self.bs[qchar] == None:
            return []
        elif type(self.bs[qchar]) == int:
            ls = len(s)
            lq = len(q)
            for i in range(depth, lq):
                j = self.bs[qchar] + self.true_depth + i
                if j >= ls or s[j] != q[i]:
                    return []
            j = self.bs[qchar] + lq
            if (not ends_in_space) or j >= s or (not s[j].isspace()):
                return [self.bs[qchar]]
            else:
                return []
        else:
            return self.bs[qchar].get_matches(s, q, depth+1, ends_in_space)

    def get_matches_within_dist(self, s, q, dist, depth, ends_in_space):
        if depth == len(q):
            return self.scrape_node(ends_in_space)
        qchar = q[depth]
        matches = []
        for item in self.bs.items():
            schar = item[0]
            v = item[1]
            if type(v) == int:
                q_remaining = len(q) - depth
                sub_start = v + self.true_depth
                sub_end = sub_start + q_remaining
                substring = s[sub_start: sub_end]
                ed = edit_dist(substring, q[depth:])
                if ed <= dist:
                    # TODO: space might occur before s[sub_end]
                    if (not ends_in_space) or sub_end >= len(s) or s[sub_end].isspace():
                        matches.append(v)
            elif isinstance(v, TrieNode):
                child = v
                eq = equal(schar, qchar)
                if dist > 0:
                    # insert schar
                    matches += child.get_matches_within_dist(s, q, dist-1, depth, ends_in_space)
                    # delete qchar
                    matches += self.get_matches_within_dist(s, q, dist-1, depth+1, ends_in_space)
                    # replace qchar with schar
                    matches += child.get_matches_within_dist(s, q, dist-eq, depth+1, ends_in_space)
                elif eq == 0:
                    # match qchar and schar
                    matches += child.get_matches_within_dist(s, q, dist, depth+1, ends_in_space)

        return matches

    def scrape_node(self, ends_in_space):
        if not ends_in_space:
            return self.scrape_node_helper()
        else:
            matches = []
            if type(self.bs[' ']) == int:
                matches.append(self.bs[' '])
            elif isinstance(self.bs[' '], TrieNode):
                matches += self.bs[' '].scrape_node_helper()
            if type(self.bs['\0']) == int:
                matches.append(self.bs['\0'])
            return matches

    def scrape_node_helper(self):
        indices = []
        for v in self.bs.values():
            if type(v) == int:
                indices.append(v)
            elif isinstance(v, TrieNode):
                indices += v.scrape_node_helper()
        return indices

    def get_subtrie_depth(self, depth):
        subnodes = [v for v in self.bs.values() if v is not None and type(v) != int]
        if not subnodes:
            return depth
        return max(node.get_subtrie_depth(depth+1) for node in subnodes)




