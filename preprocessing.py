import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import string
import json
import jsonlines
import nltk
import re

nltk.download('vader_lexicon')

from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def remove_noise(tweet_text):
    tweet_text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet_text)
    tweet_text = re.sub('@[^\s]+', 'AT_USER', tweet_text)
    tweet_text = re.sub(r'#([^\s]+)', r'\1', tweet_text)
    return tweet_text

df1 = pd.DataFrame([],columns=['id','text','created_at', 'created_at_time', 'city_name','country','sentiment'])
with jsonlines.open('/content/drive/MyDrive/Colab Notebooks/tweets2.jsonl') as reader:
    for obj in reader:
      tweet_text = obj['text'].lower() #normalizing
      tweet_text = remove_noise(tweet_text) # removing noise
      tweet_text = word_tokenize(tweet_text) # tokening the text
      # filtering
      tweet_created_at = obj['created_at']
      id = obj['id']
      place = obj['place']
      city_name = place['name']
      country = place['country']
      new_df = pd.DataFrame([[id, tweet_text, tweet_created_at, 0, city_name, country, 0]],
        columns=['id','text','created_at', 'created_at_time', 'city_name','country', 'sentiment'])
      df1 = df1.append(new_df)
    df1 = df1.reset_index(drop=True)
    print(df1)