import time
import datetime

negative_count = 0
positive_count = 0
neutral_count = 0
for index, row in df1.iterrows():
  score = SentimentIntensityAnalyzer().polarity_scores(row['text'])
  if score['neg'] > 0.25:
    row['sentiment'] = -1
    negative_count = negative_count +1
  elif score['pos'] > 0.25:
    row['sentiment'] = 1
    positive_count = positive_count + 1
  else:
    row['sentiment'] = 0
    neutral_count = neutral_count + 1
  row['created_at_time'] = time.mktime(datetime.datetime.strptime(row['created_at'], "%a %b %d %H:%M:%S +0000 %Y").timetuple())