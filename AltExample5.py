# Answer to a question on Flask mailing list
# http://librelist.com/browser//flask/2012/6/30/using-ajax-with-flask/
# NOTE: *REALLY* don't do the thing with putting the HTML in a global
#       variable like I have, I just wanted to keep everything in one
#       file for the sake of completeness of answer.
#       It's generally a very bad way to do things :)
#
from flask import (Flask, jsonify, render_template)
from twitter_streamer import StdOutListener
from tweepy import Stream, OAuthHandler
from config import consumer_key, consumer_secret, access_token, access_token_secret

app = Flask(__name__)

#Twitter Credentials
consumer_key = consumer_key
consumer_secret = consumer_secret
access_token = access_token
access_token_secret = access_token_secret

# OAuth process
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

l = StdOutListener()

@app.route('/')
def index():
    return render_template('newindex2.html')

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

