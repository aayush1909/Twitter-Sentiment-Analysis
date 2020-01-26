import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):

    def __init__(self):
        consumer_key = '##'
        consumer_secret = '##'
        access_token = '##'
        access_token_secret = '##'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        print('\nTweet is: \n', tweet, '\n', analysis.sentiment)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        tweets = []

        try:
            fetched_tweets = self.api.search(q=query, count=count)

            for tweet in fetched_tweets:
                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def main():
    api = TwitterClient()
    tweets = api.get_tweets(query='football', count=200)

    print('\n\n---------------------------------------------------------------------------------------------\n')
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    print("Neutral tweets percentage: {} % ".format(100 * (len(tweets) - len(ptweets) - len(ntweets)) / len(tweets)))

    print('\n\n---------------------------------------------------------------------------------------------\n')
    print("\t\t\t\t\tPOSITIVE TWEETS")
    for tweet in ptweets[:10]:
        print('\nTweet: \n', tweet['text'])

    print('\n\n---------------------------------------------------------------------------------------------\n')
    print("\t\t\t\t\tNEGATIVE TWEETS")
    for tweet in ntweets[:10]:
        print('\nTweet: \n', tweet['text'])

    print('\n\n---------------------------------------------------------------------------------------------\n')
    print("\t\t\t\t\tNEUTRAL TWEETS")
    for tweet in neutweets[:10]:
        print('\nTweet: \n', tweet['text'])


if __name__ == "__main__":
    main()