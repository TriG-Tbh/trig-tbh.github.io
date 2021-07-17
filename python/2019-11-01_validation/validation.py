import praw
import datetime
import time
import os

reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')

os.system("clear")
sub_name = input("Subreddit name: r/")

os.system("clear")


option = int(input("1: Get new posts\n2: Check posts\nSelect an option: "))

os.system("clear")


def compare(l1, l2):
    similar = 0
    for item in l1:
        if item in l2:
            similar += 1
    return similar


limit = 500

wait = 5  # In minutes
wait *= 60


sub = reddit.subreddit(sub_name)

firsttime = True

if option == 1:
    bad = []
    for post in sub.hot(limit=limit):
        if post.over_18:
            bad.append(post.id)
    print("Posts: \n" + ", ".join(bad))


elif option == 2:
    old = input("List: ")
    os.system("clear")
    old = old.strip()
    old = old.replace("'", "")
    old = old.replace("[", "")
    old = old.replace("]", "")
    old = list(old.split(", "))
    new = []
    for post in sub.hot(limit=limit):
        if post.over_18:
            new.append(post.id)
    similar = compare(old, new)
    if similar > 0:
        print("{} similar posts found".format(similar))
    else:
        print("No similar posts")
    print("Old: " + ", ".join(old))
    print("New: " + ", ".join(new))
