# Data Structures for use in Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com

from helper import get_lines_from_raw_twitter_data
from helper import reduce_str, process_loc
from distance import edit_dist, equal, sub_edit_dist

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
        return max(k for k in d.keys() if k <= index)

    def get_tweet_from_id(self, id):
        if id in self.id_to_tweet:
            return self.id_to_tweet[id]

    def get_location_from_id(self, id):
        if id in self.id_to_loc:
            return self.id_to_loc[id]

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
        ms = self.root.get_matches_within_dist(self.s, q, dist, dist, 0, ends_in_space)
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
                index = self.bs[qchar]
                length = self.true_depth
                return [Match(index, length)]
            else:
                return []
        else:
            return self.bs[qchar].get_matches(s, q, depth+1, ends_in_space)

    def get_matches_within_dist(self, s, q, true_dist, dist, depth, ends_in_space):
        if dist < 0:
            return []
        matches = []
        if depth >= len(q):
            matches += self.scrape_node(ends_in_space)
            for (schar, v) in self.bs.items():
                if type(v) == int:
                    index = v
                    length = depth
                    matches.append(Match(index, length))
                elif isinstance(v, TrieNode):
                    matches += v.get_matches_within_dist(s, q, true_dist, dist-1, depth+1, ends_in_space)
            return matches
        qchar = q[depth]
        if dist > 0:
            # add matches for deleting qchar
            matches += self.get_matches_within_dist(s, q, true_dist, dist-1, depth+1, ends_in_space)
        for item in self.bs.items():
            schar = item[0]
            v = item[1]
            if type(v) == int:
                subq = q[depth:]
                sub_start = v + self.true_depth
                sub_end = min(sub_start + len(subq) + dist, len(s))
                # if we want our substring to end in a space, reduce sub_end
                # so that the character after substring is either string end or space
                if ends_in_space:
                    if sub_end < len(s):
                        while sub_end >= 0 and not s[sub_end].isspace():
                            sub_end -= 1
                    # make sure we haven't reduced it so far that it would take more
                    # than true_dist chars to even increase the length of substring to q
                    if len(subq) - (sub_end-sub_start) > dist:
                        continue
                substring = s[sub_start: sub_end]
                
                ed, sub_len = sub_edit_dist(substring, subq, ends_in_space)
                # ed = edit_dist(substring, q[depth:])
                if ed <= dist:
                    sub_end = sub_start + sub_len
                    sub_len += self.true_depth
                    if (not ends_in_space) or sub_end >= len(s) or s[sub_end].isspace():
                        index = v
                        matches.append(Match(index, sub_len))
            elif isinstance(v, TrieNode):
                child = v
                eq = equal(schar, qchar)
                if dist > 0:
                    # insert schar
                    matches += child.get_matches_within_dist(s, q, true_dist, dist-1, depth, ends_in_space)
                    # replace qchar with schar
                    matches += child.get_matches_within_dist(s, q, true_dist, dist-eq, depth+1, ends_in_space)
                elif eq == 0:
                    # match qchar and schar
                    matches += child.get_matches_within_dist(s, q, true_dist, dist, depth+1, ends_in_space)
        return matches

    def scrape_node(self, ends_in_space):
        length = self.true_depth
        if not ends_in_space:
            return self.scrape_node_helper(length)
        else:
            matches = []
            for k in ' \0':
                if type(self.bs[k]) == int:
                    index = self.bs[k]
                    matches.append(Match(index, length))
                elif isinstance(self.bs[k], TrieNode):
                    matches += self.bs[k].scrape_node_helper(length)
            return matches

    def scrape_node_helper(self, length, scrape_depth=None):
        if scrape_depth == 0:
            return []
        matches = []
        for v in self.bs.values():
            if type(v) == int:
                index = v
                matches.append(Match(index, length))
            elif isinstance(v, TrieNode):
                if scrape_depth:
                    matches += v.scrape_node_helper(length=length, scrape_depth=scrape_depth-1)
                else:
                    matches += v.scrape_node_helper(length=length)
        return matches

    def get_subtrie_depth(self, depth):
        subnodes = [v for v in self.bs.values() if v is not None and type(v) != int]
        if not subnodes:
            return depth
        return max(node.get_subtrie_depth(depth+1) for node in subnodes)

class Match():
    def __init__(self, index, length, string=None, tweet_id=None, loc=None, true_loc=None):
        self.index = index
        self.length = length
        self.string = string
        self.tweet_id = tweet_id
        self.loc = loc # this is the query which we've matched
        self.true_loc = true_loc # this is the location where the tweeter is

    def set_string(self, string):
        self.string = string

    def set_tweet_id(self, tweet_id):
        self.tweet_id = tweet_id

    def set_loc(self, loc):
        self.loc = loc

    def set_true_loc(self, true_loc):
        self.true_loc = true_loc

    def __eq__(self, other):
        if not isinstance(other, Match):
            return false
        return self.index == other.index and self.length == other.length

    def __hash__(self):
        return self.index ^ self.length




