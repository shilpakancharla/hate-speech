import mysql
import parser
import tweepy
from private.keys import api_key, api_secret_key, access_token, access_token_secret

"""
    Upon receiving information about the API keys from Twitter, this section will become active. For now,
    it acts as a placeholder.
"""
authentication = tweepy.OAuthHandler(api_key, api_secret_key)
authentication.set_access_token(access_token, access_token_secret)
MyListener = MyListener(api=tweepy.API(authentication, wait_on_rate_limit=True))
myStream = tweepy.Stream(auth = api.auth, listener = MyListener)
myStream.filter(languages=["en"], track=['#islam'])

# Customize stream listener to add extra conditions
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            # Decode JSON from Twitter
            datajson = json.loads(data)
            # Get wanted data from the Tweet
            id_str = datajson['id_str']
            print(1)
            created_at = parser.parse(datajson['created_at'])
            created_at = datajson['created_at']
            print(2)
            text = datajson['text']
            text = removeEmoji(text)
            print(3)
            user_created_at = parser.parse(datajson['user_created_at'])
            processed = -1
            print(4)
            user_location = datajson['user_location']
            print(5)

            # Print out a message regarding when data was collected
            print("Tweet collected at " + str(text))

            # Insert data into MySQL database
            store_data(id_str, created_at, text, processed)
            print(datajson)
        except Exception as e:
            print(e)

    # Create function to store data in MySQL database
    def store_data(self, id_str, created_at, text, processed):
        db = mysql.connector.connect(host="localhost", user="root",  passwd="password", db="twitter_2", charset="utf8")
        cursor = db.cursor()
        insert_query = "INSERT INTO twitter_2 (id_str, created_at, text, processed) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (id_str, created_at, text, processed))
        db.commit()
        cursor.close()
        db.close()
        return
