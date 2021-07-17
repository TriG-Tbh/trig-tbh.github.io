import os
import praw

reddit = praw.Reddit(client_id="[REDACTED]",
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')

os.system("cls")

name = input("Username: u/")

user = reddit.redditor(name)
for post in user.submissions.new(limit=None):
    if not post.over_18:
        print(post.title + "\n" + "https://www.reddit.com" +
              post.permalink + "\n" + post.url if not post.is_self else "")
        print()

print("-"*25)

for post in user.submissions.new(limit=None):
    if post.over_18:
        # print(post.title + "\n" + "https://www.reddit.com" +
        #      post.permalink + "\n" + post.url if not post.is_self else "")
        print(post.title + "\n" + "https://www.reddit.com" +
                post.permalink + "\n" + post.url if not post.is_self else "")
        print()