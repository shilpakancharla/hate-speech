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