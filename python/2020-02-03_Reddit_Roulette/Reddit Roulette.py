import random

import os, sys
import platform
def clear():
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        os.system("clear")
    elif plt == "Windows":
        os.system("cls")
    else:
        pass

import praw
reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')

clear()
sub = input("Subreddit name: r/")
try:
    for _ in reddit.subreddit(sub).top(limit=1):
        pass
except:
    input("Subreddit r/" + sub + " does not exist. Press enter to continue. ")
    sys.exit(1)

posts = []

limit = 50

subreddit = reddit.subreddit(sub)

clear()
print("Collecting posts...")
for post in subreddit.hot(limit=limit):
    posts.append(post)

clear()

print("Shuffling...")
for i in range(random.randint(5, 25)):
    random.shuffle(posts)

clear()

post = input("Choose a number from 1-{}: ".format(limit))
post = int(post)
if post < 1 or post > limit:
    sys.exit(1)

post -= 1
post = posts[post]
clear()
print(("NSFW - " if post.over_18 else "") + post.title)
if not post.is_self:
    print("https://www.reddit.com" + post.permalink)
