from flask import (Flask, jsonify, render_template)
from twitter_streamer import StdOutListener
from tweepy import Stream, OAuthHandler
# from config import consumer_key, consumer_secret, access_token, access_token_secret

app = Flask(__name__)

# Twitter Credentials**
# Mine are imported from a private file, feel free to plug
# in yours using the following code:

consumer_key = 'my consumer key string'
consumer_secret = 'my consumer secret string'
access_token = 'my access token string'
access_token_secret = 'my access token secret'

# consumer_key = consumer_key
# consumer_secret = consumer_secret
# access_token = access_token
# access_token_secret = access_token_secret

# OAuth process
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

l = StdOutListener()

@app.route('/')
def index():
    return render_template('newindex3.html')

@app.route('/ajax', methods=['POST'])
def ajax_request():
    stream = Stream(auth, l)
    stream.filter(track=['Trump'], async=True)
    score = round(l.df.Sentiment.mean(), 4)
    numTweets = len(l.df)
    return jsonify(score=score, numTweets = numTweets)

if __name__ == "__main__":
    app.run(debug=True)


# 1. Integrate Spinner with Sentiment Score
# 2. Begin UI/UX Design

