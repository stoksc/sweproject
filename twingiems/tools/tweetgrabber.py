''' This module provides functions that use a tweepy api to returns tweets by a user
or hashtag.

TODO:
  * need to start adding in type annotations
'''

import tweepy


def get_tweets_from_user(screen_name, api, count=200):
    ''' Receives a screen name to query and a tweepy api object. Uses this
    information to return tweets from this user.
    '''
    tweets = api.user_timeline(screen_name=screen_name, count=count)
    return [clean_tweet(tweet) for tweet in tweets]


def get_tweets_with_hashtag(hashtag, api, count=10, lang='en'):
    ''' Receives a hashtag to query, a tweepy api object, the number of tweets
    to grab and the language. Uses this information to return tweets with this hashtag.
    '''
    tweets = tweepy.Cursor(api.search,
                           q="#{}".format(hashtag),
                           count=count,
                           lang=lang)
    return [clean_tweet(tweet) for tweet in tweets.items()]


def clean_tweet(tweet):
    ''' Takes a tweepy tweet object and returns a dictionary that contains
    the information from the tweet that we actually need.
    '''
    tweet_data = {
        'user' : tweet.user.screen_name,
        'time' : tweet.created_at,
        'text' : tweet.text,
        'timezone' : tweet.user.time_zone,
        'hashtags' : tweet.entities['hashtags'],
    }

    if hasattr(tweet, 'favorite_count'):
        tweet_data['favorites'] = tweet.favorite_count
    else:
        tweet_data['favorites'] = 0

    if hasattr(tweet, 'retweet_count'):
        tweet_data['retweets'] = tweet.retweet_count
    else:
        tweet_data['retweets'] = 0

    if hasattr(tweet, 'reply_count'):
        tweet_data['replies'] = tweet.reply_count
    else:
        tweet_data['replies'] = 0

    return tweet_data