import tweepy
from tweepy.streaming import StreamListener
import json


# Put your own secrets in:
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

LOCATION_BOX = [-180, -90, 180, 90]
TWITTER_CACHE = '.twitter_cache'


class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        if data.get('coordinates'):
            with open(TWITTER_CACHE, 'a') as fout:
                fout.write(json.dumps(data) + '\n')
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)

    stream = tweepy.Stream(auth, listener)
    stream.filter(locations=LOCATION_BOX)
