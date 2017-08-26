#Imports
import redis
import pandas as pd
import datetime
import json
from tweepy.streaming import StreamListener
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

red = redis.StrictRedis()

#Create Stream Listener
class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.colNames = ("Time", "RealTime", "Text", "Sentiment")
        self.df = pd.DataFrame(columns = self.colNames)
        self.analyzer = SentimentIntensityAnalyzer()
    def on_data(self, data):
        try:
            tweet = json.loads(data)
            tweet = [(tweet['created_at'], time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),
                      tweet["text"],float(self.analyzer.polarity_scores(tweet["text"])['compound']))]

            # Transfer Tweet
            df_temp = pd.DataFrame(tweet, columns=self.colNames)
            self.df = self.df.append(df_temp)


            # Reset Index and RealTime
            self.df.RealTime = pd.to_datetime(self.df.RealTime)
            self.df = self.df.reset_index(drop=True)

            # Keep Only Last 10 Minutes
            currentTime = self.df.RealTime.max()
            xMinAgoTime = currentTime - datetime.timedelta(minutes=10)
            self.df = self.df.loc[self.df['RealTime'] > xMinAgoTime]
            print('Success: ', len(self.df))
        except BaseException as e:
            print('Failed: ', str(e))
            time.sleep(1)

    def on_error(self, status):
        print('Error: ', status)

