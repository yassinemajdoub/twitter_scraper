import tweepy
import pandas as pd
import datetime
from more_itertools import chunked

# consumer_key = 'EBl9HKwi0eI3LWlWbXVHaRGgR'
# consumer_secret = 'SWPEKOlGNOP3C2ogecs4eFJw1Km4V8D1cJxcFepiiq01mTg1Na'
# access_token = '1582434469302206465-19LSdugdKbkIw0euEum16XsYEFmLt1'
# access_token_secret = 'B2bCjqHbQHxOy7smZTsHuLkHvS1cYEyLhSWPH8CUp8xXh'

bearer_token = 'token_here'
client = tweepy.Client(bearer_token=bearer_token)

# auth = tweepy.OAuth1UserHandler(
#     consumer_key,
#     consumer_secret,
#     access_token,
#     access_token_secret
# )

# client = tweepy.Client(auth)

start_date = datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
end_date = datetime.datetime(2022, 2, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
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
    tweets += response.data
    for tweet in response.data:
        tweets_ids.append(tweet.id)
    if "next_token" in response.meta:
        pagination_token = response.meta["next_token"]
    else:
        break


# Split the tweet IDs into chunks of 100
id_chunks = list(chunked(tweets_ids, 10))


for chunk in id_chunks:
    tweets_info = client.get_tweets(ids=chunk, tweet_fields=["created_at", "public_metrics","text"])
    
    print("this is tweets info ",tweets_info)

    for tweet in tweets_info[0]:
        print(f"ID: {tweet['id']}")
        print(f"Text: {tweet['text']}")
        print(f"Date: {tweet['created_at']}")
        print("Public metrics\n")
        print(f"Likes: {tweet['public_metrics']['like_count']}")
        print(f"Retweets: {tweet['public_metrics']['retweet_count']}")
        print(f"reply_count: {tweet['public_metrics']['reply_count']}")
        print(f"quote_count: {tweet['public_metrics']['quote_count']}")
        # print("non_public_metrics\n") 
        # print(f"impression_count: {tweet['non_public_metrics']['impression_count']}")
        # print(f"url_link_clicks: {tweet['non_public_metrics']['url_link_clicks']}")
        # print(f"user_profile_clicks: {tweet['non_public_metrics']['user_profile_clicks']}")




# # Create a DataFrame from the tweets
# df = pd.DataFrame(tweets)

# # Select the columns to include in the Excel file
# cols = ['id', 'created_at', 'text', 'favorite_count', 'retweet_count']

# # Reorder the columns if needed
# df = df[cols]

# # Export the DataFrame to an Excel file
# file_name = 'tweets.xlsx'
# df.to_excel(file_name, index=False)