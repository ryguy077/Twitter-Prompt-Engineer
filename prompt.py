import json

def load_tweets_from_json(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)

def process_tweet_text(text):
    text = text.replace('\n', ' ').replace('\r', '').replace('&amp;', '&').strip()
    return text

def is_valid_tweet(text):
    if text.startswith("RT") or text.startswith("@"):
        return False
    return True

def create_gpt_prompt(tweets):
    prompt = "Please analyze the following tweets and create new tweets that can get high engagement:\n\n"
    
    processed_tweets = set()
    
    for tweet in tweets:
        text = process_tweet_text(tweet["text"])
        
        if not is_valid_tweet(text) or text in processed_tweets:
            continue
        
        processed_tweets.add(text)
        likes = tweet["public_metrics"]["like_count"]
        retweets = tweet["public_metrics"]["retweet_count"]
        prompt += f"- Tweet: {text} | Likes: {likes} | Retweets: {retweets}\n"

    prompt += "\nNew high-engagement tweets:\n"
    return prompt

if __name__ == "__main__":
    tweets = load_tweets_from_json("tweets.json")
    prompt = create_gpt_prompt(tweets)
    print(prompt)