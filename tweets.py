import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load Twitter API credentials
API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET_KEY = os.environ["TWITTER_API_SECRET_KEY"]
BEARER_TOKEN = os.environ["TWITTER_BEARER_TOKEN"]

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}

# Function to filter tweets
def filter_tweets(tweet, users):
    banned_words = ["giveaway", "free", "bot"]
    user = users[tweet["author_id"]]
    for word in banned_words:
        if word in tweet["text"].lower() or word in user["username"].lower():
            return False
    if "retweeted_status" in tweet:
        return False
    return True

# Function to get tweets
def get_tweets(usernames, count):
    tweets = []
    for username in usernames:
        url = f"https://api.twitter.com/2/users/by/username/{username}"
        user = requests.get(url, headers=headers)
        user_id = user.json()["data"]["id"]

        url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={count}&expansions=author_id&user.fields=username&tweet.fields=public_metrics,conversation_id"
        response = requests.get(url, headers=headers)
        response_data = response.json()
        user_tweets = response_data["data"]
        users = {user["id"]: user for user in response_data["includes"]["users"]}

        filtered_tweets = [t for t in user_tweets if filter_tweets(t, users) and t.get("in_reply_to_user_id") is None]
        tweets.extend(filtered_tweets)
    return tweets

# Function to search tweets
def search_tweets(query, count):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={count}&expansions=author_id&user.fields=username&tweet.fields=public_metrics,conversation_id"
    response = requests.get(url, headers=headers)
    response_data = response.json()

    if "data" not in response_data:
        return []

    search_tweets = response_data["data"]
    users = {user["id"]: user for user in response_data["includes"]["users"]}

    filtered_tweets = [t for t in search_tweets if filter_tweets(t, users) and t.get("in_reply_to_user_id") is None]

    # Fetch threaded replies
    threaded_tweets = []
    for tweet in filtered_tweets:
        conversation_id = tweet["conversation_id"]
        user_id = tweet["author_id"]
        url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{users[user_id]['username']} conversation_id:{conversation_id}&max_results={count}&expansions=author_id&user.fields=username&tweet.fields=public_metrics,conversation_id"
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if "data" not in response_data:
            continue

        thread_tweets = response_data["data"]
        users.update({user["id"]: user for user in response_data["includes"]["users"]})

        for t in thread_tweets:
            if filter_tweets(t, users) and t.get("in_reply_to_user_id") is not None:
                threaded_tweets.append(t)

    return filtered_tweets + threaded_tweets

    # Fetch threaded replies
    threaded_tweets = []
    for tweet in filtered_tweets:
        conversation_id = tweet["conversation_id"]
        user_id = tweet["author_id"]
        url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{users[user_id]['username']} conversation_id:{conversation_id}&max_results={count}&expansions=author_id&user.fields=username&tweet.fields=public_metrics,conversation_id"
        response = requests.get(url, headers=headers)
        response_data = response.json()
        thread_tweets = response_data["data"]
        users.update({user["id"]: user for user in response_data["includes"]["users"]})

        for t in thread_tweets:
            if filter_tweets(t, users) and t.get("in_reply_to_user_id") is not None:
                threaded_tweets.append(t)

    return filtered_tweets + threaded_tweets

# Function to load existing tweets from JSON
def load_existing_tweets(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to append tweets to JSON
def append_tweets_to_json(tweets, file_name):
    existing_tweets = load_existing_tweets(file_name)
    existing_tweet_ids = {t["id"] for t in existing_tweets}

    new_tweets = [t for t in tweets if t["id"] not in existing_tweet_ids]
    all_tweets = existing_tweets + new_tweets

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(all_tweets, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    users = ["BitGod21", "JussCubs", "dochollywoodart", "LeonidasNFT", "ZK_shark", "OrdinalMaxiBiz", "BitcoinFrogs", "0xBigL", "BRC20Coins"]
    tweets = get_tweets(users, 20)
    search_results = search_tweets("brc-20 thread", 20)
    all_tweets = tweets + search_results
    append_tweets_to_json(all_tweets, "tweets.json")