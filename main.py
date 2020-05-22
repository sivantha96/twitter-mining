import os
import re
from tweepy import Cursor
from tweepy import API
from tweepy import OAuthHandler
import pandas as pd
import pandas.io.excel._xlsxwriter as xlsxwriter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# function to get the authentication with the given credentials
def get_twitter_authentication():
        consumer_key = os.environ.get('TWITTER_API_KEY')
        consumer_secret = os.environ.get('TWITTER_API_SECRET')
        auth = OAuthHandler(consumer_key, consumer_secret)
        return auth

# function to get the Twitter API client
def get_twitter_client():
    # get authentication
    auth = get_twitter_authentication()
    # create Twitter API
    client = API(auth)
    return client

# function to get the twitter data 
def get_twitter_data(search_query, number_of_tweets, geocode, date_before):
    # get Twitter API
    api = get_twitter_client()
    # object to hold all the tweets
    tweet_objects = []
    # Search for a specific keyword and iterate through the results
    for tweet in Cursor(
        api.search,
        q=search_query,
        count=number_of_tweets,
        geocode=geocode,
        result_type="recent",
        until=date_before,
    ).items():
        # csvWriter.writerow([tweet.id, tweet.created_at, tweet.text, tweet.truncated, tweet.user.id, tweet.user.location, tweet.user.verified, tweet.user.follors_count, ])
        tweet_objects.append(tweet)
    return tweet_objects

count = 0

# function to convert the list of objects to a pandas dataframe
def get_converted_dataframe(tweet_objects):
    
    df = pd.DataFrame()
    prev_attr = "tweet"
    for tweet in tweet_objects:
        global count 
        count = 0
        df_row = pd.DataFrame()
        df_row = add_to_df(tweet._json, prev_attr + "_", df_row)
        df = pd.concat([df, df_row], ignore_index=True, sort=False)
    return df


# function that append value into the dataframe recursively
def add_to_df(obj, pre_attr, df_row):
    
    for attr, value in obj.items():
        if type(value) is dict:
            df_row = add_to_df(value, pre_attr + attr + "_", df_row)
        elif type(value) is list:
            continue
            # dddd
        else:
            global count
            seriesValue = pd.Series([])
            seriesValue[0] = value
            isDuplicate = False
            for col in df_row.columns:
                if pre_attr + attr == col:
                    isDuplicate = True
                else:
                    continue
            if isDuplicate == True:
                df_row.insert(count,  str(count) + pre_attr + attr, seriesValue)
            else:
                df_row.insert(count,  pre_attr + attr, seriesValue)
            count = count + 1
    return df_row

# function to preprocess the given tweet data
def clean_tweets(tweet_text):
    tweet_text = tweet_text.lower() # normalizing
    tweet_text = remove_noise(tweet_text) # removing noise
    tweet_text = word_tokenize(tweet_text) # tokening the text
    return tweet_text

def remove_noise(tweet_text):
    tweet_text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet_text)
    tweet_text = re.sub('@[^\s]+', 'AT_USER', tweet_text)
    tweet_text = re.sub(r'#([^\s]+)', r'\1', tweet_text)
    return tweet_text

def save_dataframe(df, name):
    writer = pd.ExcelWriter( name , engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Twitter data')
    writer.save()

if __name__ == "__main__":
    # define arguments to pass
    search_query = "curfew"
    number_of_tweets = 100
    geocode = "7.8731,80.7718,224km"  # latitude:7.8731, longitude:80.7718, radius:224km
    date_before = "2020-05-22"
    # get twitter data
    tweet_objects = get_twitter_data(
        search_query, number_of_tweets, geocode, date_before
    )

    # get a pandas dataframe from the Twitter data
    df = get_converted_dataframe(tweet_objects)

    # save the original dataframe in an excel sheet
    save_dataframe(df, "tweets_original.xlsx")

    # handle missing values
    df = df.fillna("undefined") # fill missing values

    # save the modified dataframe in an excel sheet
    save_dataframe(df, "tweets_no_nan.xlsx")

    # extracting id and the text field from the data frame
    df_text = df[['tweet_id', 'tweet_text']]

    # Clean textual data
    df_text['tweet_text'] = df_text['tweet_text'].apply(clean_tweets)

    # save the modified dataframe in an excel sheet
    save_dataframe(df, "tweets_clean.xlsx")

    
    