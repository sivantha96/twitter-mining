import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

total_count = positive_count + neutral_count + negative_count
positive_percentage = round((positive_count / total_count)*100, 2)
neutral_percentage = round((neutral_count / total_count)*100, 2)
negative_percentage = round((negative_count / total_count)*100, 2)

labels = ['Positive [' + str(positive_percentage) + '%]' , 'Neutral [' + str(neutral_percentage) + '%]', 'Negative [' + str(negative_percentage) + '%]']
sizes = [positive_count, neutral_count, negative_count]
colors = ['yellow', 'blue','red']
patches, texts = plt.pie(sizes,colors=colors, startangle=90)
plt.style.use('default')
plt.legend(labels)
plt.title('Sentiment Distribution')
plt.axis('equal')
plt.show()

df1.to_csv('dataframe.csv')

df1['created_at'] = pd.to_datetime(df1['created_at'])

counts = pd.Series(index=df1.created_at, data=np.array(df1.sentiment)).resample('D').count()

counts

counts.plot() 
plt.show()

counts2 = pd.Series(index=df1.created_at, data=np.array(df1.sentiment)).resample('D').sum()

print(counts2)

counts2.plot() 
plt.show()