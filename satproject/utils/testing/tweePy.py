import tweepy
import logging

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


def percentage(part,whole):
 return 100 * float(part)/float(whole)


def fetchTweets(topic, numTweets):
    # note: change max tokenization length if using visual studio IDE 
    # https://stackoverflow.com/questions/66287172/tokenization-is-skipped-for-long-lines-for-performance-reasons-the-length-of-a
    
    #setup logging
    logging.basicConfig(filename='tweePy_raw.log', encoding='utf-8', level=logging.DEBUG)

    #authenticate inorder to use twitter api calls
    auth = tweepy.OAuth1UserHandler(
    "ohYzj0IJppr5rJl1h8VLrmUMo", "tMpA64mq3TkDcmLHJuouymymG7YoBsbE41jF3Y0mLYvENwN7Sj",
    "1578234284330065921-Cl3mENupTVd0BypLDUDdvqpbq661Y1", "dVqPENfbcvKv7bZ8W6mC9Lb7zB6h1qUHMsbYouqZg3vPx")
    #get instance of api to be able to make queries such as search tweets call
    api = tweepy.API(auth)

    #fetch english twitter tweet data and metadata for the given topic
    results = api.search_tweets(q=topic, count=numTweets, lang = "en", tweet_mode='extended')

    #list of pure tweet messages to be returned
    tweets = []
    logging.basicConfig(filename='tweePy_debug_text.log', encoding='utf-8', level=logging.DEBUG, force=True)
    for result in results:
        tweets.append(result.full_text)
        logging.debug(result.full_text)
    
    #return populated list
    return tweets

def getSentiment(tweets):
    positive = 0
    # consider the percentage of tweets that are positive -> score
    for tweet in tweets:
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = score['neg']
        pos = score['pos']
        if (pos > neg):
            positive += 1
    # returns percentage of positive tweets
    return percentage (positive, len(tweets))    
