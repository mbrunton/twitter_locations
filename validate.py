# Knowledge Technologies Project 1
# Mitchell Brunton #537642
# mmbrunton@gmail.com
#
# Validate that matches refer to a probable location name
#

import nltk

allowed_tags = ['FW', 'NNP', 'NNPS']

def validate_matches(ms, loc, corpus):
    valid_ms = []
    for m in ms:
        tweet_start = corpus.get_tweet_start_index_from_index(m)
        tweet_id = corpus.index_to_id[tweet_start]
        tweet = corpus.id_to_tweet[tweet_id]
        offset = m - tweet_start
        space = offset + tweet[offset:].find(' ')
        if space < 0:
            space = len(tweet)
        first_word = tweet[offset:space]
        print '\tfirst word of match: ' + first_word
        tag = nltk.pos_tag([first_word])[0][1]
        print '\tlexical category of ' + first_word,
        print ': ' + tag
        if tag in allowed_tags:
            valid_ms.append(m)
    return valid_ms


