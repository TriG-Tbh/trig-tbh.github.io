import praw
from settings import *
import sentiment as s
import os
reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')


subs = []
subreddit = "e"
while subreddit != "":
    os.system("clear")
    #print(len(subs))
    if len(subs) > 0:
        print("Current subreddits: " + ", ".join(["r/" + sub for sub in subs]))
    subreddit = input("Enter subreddit name (leave empty to exit): r/")
    if not subreddit:
        break
    try: 
        for _ in reddit.subreddit(subreddit).hot(limit=1):
            pass # Validates that subreddit exists
    except: 
        input("Subreddit with name \"r/" + subreddit + "\" not found. Press enter to continue. ")
        continue
    subs.append(subreddit)
os.system("clear")
sentiments = []
for sub in subs:
    total_sentiment = 0
    subreddit = reddit.subreddit(sub)
    postnum = 0
    i = 0
    for post in subreddit.hot(limit=LIMIT):
        os.system("clear")
        postnum += 1
        print("Getting post {} (r/{})...".format(postnum, sub))
        title = post.title
        sentiment = s.sentimentality(title)
        if sentiment["value"] != 0.0:
            total_sentiment += sentiment["value"]
        if post.is_self:
            text = post.selftext
            sentiment = s.sentimentality(text)
            if sentiment["value"] != 0.0:
                total_sentiment += sentiment["value"]
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            i += 1
            comment_text = comment.body
            sentiment = s.sentimentality(comment_text)
            if sentiment["value"] != 0.0:
                total_sentiment += sentiment["value"]
    total_sentiment = (total_sentiment/i if i > 0 else None)
    sentiments.append(total_sentiment)
os.system("clear")

for i in range(len(subs)):
    print("Subreddit: r/{}\nSentiment value: {}\nVerdict: {}\n".format(subs[i], round(sentiments[i], 2), s.parse_polarity(sentiments[i])))