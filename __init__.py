import logging

import azure.functions as func
import json
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from . import keys
import requests
import yake

kw_extractor = yake.KeywordExtractor()

webhook = 'https://api.telegram.org/bot1225878427:AAHHB4mc1siqv7dBkwJcjEMVq91MbC5xgRI/'

HEADERS = {
    'Content-type': 'application/json'
}


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = keys.consumer_key1
        consumer_secret = keys.consumer_key_secret1
        access_token = keys.access_token1
        access_token_secret = keys.access_token_secret1

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    username = req_body['message']['from']['first_name']
    chat__id = req_body['message']['from']['id']
    user_input = req_body['message']['text']
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    '''The below commented out code was for printing positive and negative code separatedly'''
    # positives = []
    # negatives = []
    #
    # for tweet in ptweets[:10]:
    #     positives.append(tweet['text'])
    #
    # for tweet in ntweets[:10]:
    #     negatives.append(tweet['text'].encode("utf-8"))
    dataTosend = {}

    if 'search' in user_input:
        search_term = user_input.split("search", 1)[1].strip()
        tweets = api.get_tweets(query=f'{search_term}', count=200)
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        p_percent = round(100 * len(ptweets) / len(tweets),3)
        n_percent = round(100 * len(ntweets) / len(tweets),3)
        
        hot_word = []
        for tweet in tweets:
            cleaned = api.clean_tweet(tweet['text'])
            print(cleaned)
            keywords = kw_extractor.extract_keywords(cleaned)
            print(keywords)
            for x in range(len(keywords)):
                if keywords[x][0] <= 0.015:
                    print(keywords[x][0])
                    hot_word.append(keywords[x][1])
        hot_strings=''           
        hot_strings=','.join(hot_word)
        print(hot_strings)
        dataTosendString = f"positive_response:{p_percent} % negative_respone:{n_percent}% \n hot_strings {hot_strings}"
        print(dataTosendString)
        json_data = {
            "chat_id": chat__id,
            "text": dataTosendString,
        }
        
        # dataTosend = {
        #     "positive_response": f'{100 * len(ptweets) / len(tweets)}',
        #     "negative_response": f'{100 * len(ntweets) / len(tweets)}'
        # }

        dataTosend = json.dumps(dataTosend)
        message_url = webhook + 'sendMessage'
        requests.post(message_url, json=json_data)

    return func.HttpResponse(
        dataTosend
    )
