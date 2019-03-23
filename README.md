# Geo Tweets

A set of scripts to capture geocoded tweets and order them by 
the emojis they use.

Start by running `harvest.py` - it will listen to the twitter
firehose 1% stream for geocoded tweets and dump them into
a `.twitter_cache` file. Chances are that by the time you
read this, twitter has stopped supporting this API and if not
you need to run this script for quite a while. A week would
be a good start.

Next up, run `summarize.py` to get produce the `tweets.txt`
file, which has one tweet per line. This makes for slightly
faster processing.

Then run `split_by_emoji.py` to extract a huge json document 
called `split_emojis.json` which has for each emoji a list of
coordinates and timestamps - the coordinates are on a 3600x1800 
grid while the timestamps are in 
