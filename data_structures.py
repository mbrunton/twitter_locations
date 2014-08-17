

class TwitterCorpus():
    def __init__(self, file):
        fd = open(file, 'r')
        id_to_tweet = {}
        index_to_id = {}

        lines = fd.readlines()
        for line in lines:
            fields = line.split('\t')
            tweet_id = fields[1]
            tweet_text = fields[2]
            id_to_tweet[tweet_id] = tweet_text

        processed_tweets_list = []
        next_index = 0
        for item in id_to_tweet.items():
            tweet_id = item[0]
            raw_tweet = item[1]
            index_to_id[next_index] = tweet_id
            processed_tweet = self.process_tweet(raw_tweet)
            processed_tweets_list.append(processed_tweet)
            next_index += len(processed_tweet)

        self.id_to_tweet = id_to_tweet
        self.index_to_id = index_to_id
        self.processed_tweets = processed_tweets_list
        self.monolith_tweet_str = ''.join(processed_tweets_list)

    def process_tweet(self, tweet):
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


class Trie():
    def __init__(self, w, abc):
        for a in w:
            if a not in abc:
                raise Exception('alphabet does not contain letter ' + a)
        self.w = w
        self.abc = abc
        self.root = TrieNode(abc, 0)
        for i in range(len(w)):
            self.root.add_suffix(w, i)
            
    def get_matches(self, s, tolerance=0):
        self.root.get_matches(self.w, s, tolerance)
        
class TrieNode():
    def __init__(self, abc, depth):
        self.abc = abc
        self.depth = depth
        self.bs = {} # branches
        for a in abc:
            self.bs[a] = None
            
    def add_suffix(self, w, i):
        # i is index of start of suffix in w
        first = w[i + self.depth]
        if self.bs[first] == None:
            self.bs[first] = i
        elif type(self.bs[first]) == int:
            old_index = self.bs[first]
            self.bs[first] = TrieNode(self.abc, self.depth+1)
            self.bs[first].add_suffix(w, old_index)
            self.bs[first].add_suffix(w, i)
        else:
            # bs[first] is another Node
            self.bs[first].add_suffix(w, i)
            
    def get_matches(self, w, q):
        if self.depth >= len(q):
            return True
        first = q[self.depth]
        if self.bs[first] == None:
            return False
        elif type(self.bs[first]) == int:
            lw = len(w)
            for i in range(len(q)):
                j = bs[first] + i
                if j >= lw:
                    return False
                if w[j] != q[i]:
                    return False
            return True
        else:
            return self.bs[first].get_matches(w, q)




