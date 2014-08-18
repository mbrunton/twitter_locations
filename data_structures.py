# Data Structures for use in Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com

from helper import get_lines_from_raw_twitter_data

class TwitterCorpus():
    def __init__(self, file):
        fd = open(file, 'r')
        id_to_tweet = {}
        index_to_id = {}

        # TODO: fix this method
        lines = get_lines_from_raw_twitter_data(fd)
        count = 0
        percent = 0
        ll = len(lines)
        for line in lines:
            fields = line.split('\t')
            tweet_id = int(fields[1])
            tweet_text = fields[2]
            id_to_tweet[tweet_id] = tweet_text
            if count % (ll/100) == 0:
                print 'at ' + str(percent) + '%'
                percent += 1
            count += 1

        processed_tweets_list = []
        next_index = 0
        count = 0
        percent = 0
        for item in id_to_tweet.items():
            tweet_id = item[0]
            raw_tweet = item[1]
            index_to_id[next_index] = tweet_id
            processed_tweet = self.process_tweet(raw_tweet)
            processed_tweets_list.append(processed_tweet)
            next_index += len(processed_tweet)
            if count % (ll/100) == 0:
                print 'at ' + str(percent) + '%'
                percent += 1
            count += 1

        self.id_to_tweet = id_to_tweet
        self.index_to_id = index_to_id
        self.processed_tweets = processed_tweets_list
        self.monolith_tweet_str = ''.join(processed_tweets_list)

    def process_tweet(self, tweet):
        lt = len(tweet)
        processed_tweet = ''
        for a in tweet:
            if a.isalpha():
                processed_tweet += a.lower()
            elif a.isspace():
                processed_tweet += ' '

        return processed_tweet.strip() + ' '

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
    def __init__(self, s, abc):
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
        percent = 0
        for i in range(ls):
            self.root.add_suffix(s, i)
            if i % (ls/100) == 0:
                print 'at ' + str(percent) + '%'
                percent += 1
            
    def get_matches(self, q, tolerance=0):
        return self.root.get_matches(self.s, q, tolerance)
        
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
            
    # TODO: include tolerance
    def get_matches(self, s, q, tolerance):
        if self.depth == len(q):
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
            return self.bs[first].get_matches(s, q, tolerance)

    def scrape_node(self):
        indices = []
        for v in self.bs.values():
            if type(v) == int:
                indices.append(v)
            elif type(v) == TrieNode:
                indices += v.scrape_node()
        return indices




