# Twitter Thread Scraper and Filter

This repository contains a Python script that scrapes and filters Twitter threads based on specific criteria. The script fetches tweets from specified users and searches for tweets containing certain keywords. It filters out tweets containing banned words, retweets, and those not part of a thread. The resulting tweets are saved in a JSON file for further analysis, such as sentiment analysis using GPT-4.

## Features

- Fetch tweets from specified users
- Search for tweets containing specific keywords
- Filter tweets based on banned words, retweets, and thread status
- Save filtered tweets in a JSON file
- Load existing tweets from a JSON file and update it with new tweets
- Perform future sentiment analysis using GPT-4 (not implemented in this script)

## Usage

1. Clone the repository and navigate to the project directory:

```
git clone https://github.com/yourusername/twitter-thread-scraper.git
cd twitter-thread-scraper
```

2. Install the required packages:

```
pip install -r requirements.txt
```

3. Set up your Twitter API credentials by creating a `.env` file with the following content:

```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET_KEY=your_api_secret_key
TWITTER_BEARER_TOKEN=your_bearer_token
```

Replace `your_api_key`, `your_api_secret_key`, and `your_bearer_token` with your actual Twitter API credentials.

4. Update the list of users and search query in `tweets.py`:

```python
users = ["BitGod21", "JussCubs", "dochollywoodart", "LeonidasNFT", "ZK_shark", "OrdinalMaxiBiz", "BitcoinFrogs", "0xBigL", "BRC20Coins"]
search_query = "brc-20 thread"
```

5. Run the script:

```
python tweets.py
```

6. The filtered tweets will be saved in a JSON file called `tweets.json`. You can use this file for further analysis, such as sentiment analysis using GPT-4.

## Contributing

Feel free to submit issues, feature requests, and pull requests to improve the script or add new features.
