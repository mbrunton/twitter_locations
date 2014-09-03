Readme file for Knowledge Technologies Project 1
author: Mitchell Brunton
email: mmbrunton@gmail.com

How to run this program:
This program was written and tested using Python 2.7
In project directory, type
    python project1.py <tweet file> <query file> (optional)<output file>
where tweet, query, and output file arguments are filenames

Expected format of input:
<tweet file> should be in the same format as the US.txt file, that is
    user_id \t tweet_id \t tweet_text
(spaces surrounding tab chars not included)
<location file> should be in the form
    location

Format of output:
if an <output file> argument is supplied, the program output will
be written to that file. Otherwise the program output will be sent
to stdout. Output will be in the form
    location1
    tweetid1
    tweetid2
    ...
for each location in <location file>

How subsamples of datasets were created during testing:
Subsamples of tweets were created using
    head -<num_tweets> training_set_tweets.txt > tweets<num_tweets>.txt
A subsample of US.txt was used, consisting of all those location names
which occurred in both US.txt and training_set_users.txt (approx. 3000)
From this, further subsamples were taken in the same manner as subsamples
of tweets

