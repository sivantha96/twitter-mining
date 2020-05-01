import os
from tweepy import Cursor
from tweepy import API
from tweepy import OAuthHandler

# authenticating with the given credentials
def get_twitter_authentication():
    try:
        # getting values(credentials) from environment variables
        # here I have used environment variables to store my credentials
        consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
        consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    except KeyError:
        print("Something went wrong while authenticating...")
    # authenticating for API request
    # I have used OAuth 2 authentications since I only need read-only access to public information
    auth = OAuthHandler(consumer_key, consumer_secret)
    return auth


def get_twitter_client():
    # get authentication
    auth = get_twitter_authentication()
    # create Twitter API
    client = API(auth)
    return client

def get_twitter_past_data():
    # get Twitter API
    api = get_twitter_client()
    # Search for a specific keyword and iterate through the results
    # here I have used below parameters to pass for the API call
    # search_query(q) = "curfew"
    # geocode = "latitude:7.8731, longitude:80.7718, radius:224km"
    # result_type = recent
    # until = 2020-04-01
    for tweet in Cursor(api.search, q="curfew", count="100", geocode="7.8731,80.7718,224km", result_type="recent", until="2020-04-01").items(100):
        print (tweet.user.id, tweet.text.encode('utf-8'))