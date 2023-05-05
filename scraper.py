import tweepy
import pandas as pd
import datetime
from more_itertools import chunked
import os

# consumer_key = 'EBl9HKwi0eI3LWlWbXVHaRGgR'
# consumer_secret = 'SWPEKOlGNOP3C2ogecs4eFJw1Km4V8D1cJxcFepiiq01mTg1Na'
# access_token = '1582434469302206465-19LSdugdKbkIw0euEum16XsYEFmLt1'
# access_token_secret = 'B2bCjqHbQHxOy7smZTsHuLkHvS1cYEyLhSWPH8CUp8xXh'

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMZHiQEAAAAAEJoYaWCpD0gQLHsSuxhqwlDyTJY%3DLNuhGwLurfxukTRoBaSUGBWC6k3U8fmiBIqfKs751qyPuGM85p'
client = tweepy.Client(bearer_token=bearer_token)

# auth = tweepy.OAuth1UserHandler(
#     consumer_key,
#     consumer_secret,
#     access_token,
#     access_token_secret
# )

# client = tweepy.Client(auth)
start_date_str = input("Enter start date (dd/mm/yyyy): ")
end_date_str = input("Enter end date (dd/mm/yyyy): ")

# parse start and end dates
start_date = datetime.datetime.strptime(start_date_str, "%d/%m/%Y")
end_date = datetime.datetime.strptime(end_date_str, "%d/%m/%Y")

start_date = start_date.replace(tzinfo=datetime.timezone.utc)
end_date = end_date.replace(tzinfo=datetime.timezone.utc)

#start_date = datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
#end_date = datetime.datetime(2022, 2, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
username = input("Enter the Twitter username: ")

#Get the user's ID
try:
    response = client.get_user(username=username)
    user_id = response.data["id"]
    print(f"User ID for '{username}': {user_id}")
except TypeError as e:
    print(f"Error: {e}")

# Get the tweets for the user within the date range
tweets = []
tweets_ids = []
pagination_token = None
while True:
    response = client.get_users_tweets(
        user_id,
        start_time=start_date,
        end_time=end_date,
        max_results=100,
        pagination_token=pagination_token
    )
    if response.data is not None:
        tweets += response.data
    else:
        print("Response data is None.")
        continue
    for tweet in response.data:
        tweets_ids.append(tweet.id)
    if "next_token" in response.meta:
        pagination_token = response.meta["next_token"]
    else:
        break


# Split the tweet IDs into chunks of 100
id_chunks = list(chunked(tweets_ids, 10))
tweets_data = []

for chunk in id_chunks:
    tweets_info = client.get_tweets(ids=chunk, tweet_fields=["created_at", "public_metrics","text"])
    #print("this is tweets info ",tweets_info)

    for tweet in tweets_info[0]:
        
        tweets_data.append({"ID": tweet["id"], "Text": tweet["text"], "Date": tweet["created_at"], "Likes": tweet["public_metrics"]["like_count"], "Retweets": tweet["public_metrics"]["retweet_count"], "Replies": tweet["public_metrics"]["reply_count"], "Quotes": tweet["public_metrics"]["quote_count"]})
        print("non_public_metrics\n") 
        print(f"impression_count: {tweet['non_public_metrics']['impression_count']}")
        print(f"url_link_clicks: {tweet['non_public_metrics']['url_link_clicks']}")
        print(f"user_profile_clicks: {tweet['non_public_metrics']['user_profile_clicks']}")

df = pd.DataFrame(tweets_data)
df["Date"] = df["Date"].dt.tz_localize(None)

filename = "tweets_data.xlsx"

if os.path.exists(filename):
    i = 1
    while True:
        new_filename = f"tweets_data_{i}.xlsx"
        if not os.path.exists(new_filename):
            filename = new_filename
            break
        i += 1
df.to_excel(filename, index=False)



# # Create a DataFrame from the tweets
# df = pd.DataFrame(tweets)

# # Select the columns to include in the Excel file
# cols = ['id', 'created_at', 'text', 'favorite_count', 'retweet_count']

# # Reorder the columns if needed
# df = df[cols]

# # Export the DataFrame to an Excel file
# file_name = 'tweets.xlsx'
# df.to_excel(file_name, index=False)