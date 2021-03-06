from flask import Flask, request, jsonify
from tweet_fetcher import connect, fetch
from transfer import train
import random

app = Flask(__name__)

help_string = '''<h3> REST API FOR TWEEPIC: </h3>
    Send JSON of keywords to https: // tweepic.herokuapp.com/keywords/
    and receive a tweet(JSON object) generated by neural networks trained on real
    world tweets on the given keywords(fetched from twitter's API)

    <br / > Payload example:
    <pre>
        [
            "river",
            "trees"
        ]
    </pre>
    '''

@app.route('/')
def hello():
    return '<h1>WELCOME TO TWEEPIC</h1>' + help_string
    


@app.route('/keywords', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            api = connect()
            data = request.get_json()
            tweets = []
            for kword in data:
                tweets.extend(fetch(api, kword))
            tweets = random.sample(tweets, len(tweets))
            generated_tweets = train('\n'.join(tweets))
        except ValueError:
            return jsonify('Please enter a number.')
        print(jsonify(generated_tweets))
        return jsonify(generated_tweets)
    else: return jsonify(help_string)


if __name__ == '__main__':
    app.run(debug=True)
