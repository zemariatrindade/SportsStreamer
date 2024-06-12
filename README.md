# Sports Content Streaming with Reddit API

This Python script streams sports content from various subreddits using the Reddit API. It connects to Euro2024, NBA, Tennis, and Copa America subreddits to gather comments and analyze them locally.

## Prerequisites

Before running the application, make sure you have created a `creds.sh` file with the following credentials:

```bash
# get the credentials from https://www.reddit.com/prefs/apps
CLIENT_ID="YOUR_CLIENT_ID"
SECRET_TOKEN="YOUR_SECRET_TOKEN"
USERNAME="YOUR_REDDIT_USERNAME"
PASSWORD="YOUR_REDDIT_PASSWORD"
```

You can obtain the required credentials by creating a Reddit app [here](https://www.reddit.com/prefs/apps).




## Installation

To install the necessary dependencies, run the following command:

```bash
pip3 install -r requirements.txt

```
This will install all the required Python packages listed in the requirements.txt file.

## Usage

To run the application, execute the following command:

```bash
python3 main.py
```

## Functionality
The script performs the following tasks:

- Connects to Reddit API to stream sports content from Euro2024, NBA, Tennis, and Copa America subreddits.
- Stores comments locally in the data/raw folder.
- Prints the number of times users refer to other users, other subreddits, or other URLs.
- Prints the top 10 important words based on TF-IDF (Term Frequency-Inverse Document Frequency) analysis.



