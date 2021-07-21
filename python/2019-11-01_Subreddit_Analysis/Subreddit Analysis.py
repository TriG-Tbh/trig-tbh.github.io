# Start time: 19:02:41 

# Import PRAW
import praw

# Import datetime
import datetime

import time

# Initialize Reddit instance
reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')

# Imports os, sys; clears the screen
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

clear()

# Ask for subreddit name
subredditname = input("Subreddit name: r/")

# Validates subreddit exists - if it doesn't, PRAW raises a search exception
try:
    for _ in reddit.subreddit(subredditname).top(limit=1):
        pass
# Exception catching
except:
    print("Subreddit \"r/" + subredditname + "\" does not exist.")
    # Exits the program
    sys.exit(1)
else:
    subreddit = reddit.subreddit(subredditname)

clear()
print("Analyzing r/" + subredditname + ", please wait...")

limit = 500

global new, hot, top, controversial

new = []
hot = []
top = []
controversial = []

now = time.time()
for post in subreddit.new(limit=limit):
    new.append(post)

for post in subreddit.hot(limit=limit):
    hot.append(post)

for post in subreddit.top(limit=limit):
    top.append(post)

for post in subreddit.controversial(limit=limit):
    controversial.append(post)

now = time.time() - now

minutes = now // 60
seconds = now % 60
seconds = str(round(seconds, 2))
hours = int(minutes // 60)
minutes = int(minutes % 60)
if len(str(minutes)) == 1:
    minutes = "0" + str(minutes)
if len(str(seconds).split('.')[0]) == 1:
    seconds = "0" + str(seconds)
if len(str(hours)) == 1:
    hours = "0" + str(hours)

now = hours + ":" + minutes + ":" + seconds

collection = "Time spent getting posts (hours : minutes : seconds): " + str(now) + "\n\n"


output = ""

output += "-----Program Information-----" + "\n"

output += "Subreddit: r/" + subredditname + "\n"
output += "Analysis taken at: " + str(datetime.datetime.now()) + "\n"
output += collection

now = time.time()

output += "-----Subreddit Information-----" + "\n"
output += "Subreddit name: r/" + subreddit.display_name + "\n"
output += "Subreddit link: https://www.reddit.com/r/" + subreddit.display_name + "\n"
output += "Date created: " + str(datetime.datetime.fromtimestamp(subreddit.created_utc)) + "\n"
output += "Members: " + str(subreddit.subscribers) + "\n"
mods = []
for mod in subreddit.moderator():
    mods.append(str(mod))
output += "Moderators: " + ", ".join(["u/" + moderator for moderator in mods]) + "\n"

output += "\n" + "-----NSFW Content-----" + "\n"

global sorts
sorts = {}
def get_numbers(parameter):
    good = 0
    questionable = 0
    bad = 0
    number = 1
    offenders = []
    if parameter == "hot":
        method = hot
    elif parameter == "top":
        method = top
    elif parameter == "controversial":
        method = controversial
    elif parameter == "new":
        method = new
    for post in method:
        if post.over_18:
            bad += 1
            offenders.append(post)
        elif post.link_flair_text == "Questionable" and not post.is_self:
            questionable += 1
            offenders.append(post)
        else:
            good += 1
        number += 1
    sorts[parameter] = bad / (bad + good + questionable)
    if questionable > 0:
        sorts[parameter + " (Questionable)"] = questionable / (bad + good + questionable)
    
get_numbers("hot")
get_numbers("new")
get_numbers("top")
get_numbers("controversial")


for item in sorts:
    addition = (item.title() + ": " + str(round(sorts[item] * 100, 3)) + "% chance of viewing {} post\n".format("NSFW" if "Questionable" not in item else "Questionable"))
    output += addition

output += "\n" + "-----Shared Posts-----" + "\n"


newhot = 0
hottop = 0
newcont = 0
conthot = 0

for post in new:
    if post in hot:
        newhot += 1

for post in new:
    if post in controversial:
        newcont += 1

for post in hot:
    if post in top:
        hottop += 1


for post in hot:
    if post in controversial:
        conthot += 1

output += "Percent of posts in Hot and New: {}%".format(str(round(newhot / 500, 2))) + "\n"
output += "Percent of posts in Hot and Top: {}%".format(str(round(hottop / 500, 2))) + "\n"
output += "Percent of posts in Hot and Controversial: {}%".format(str(round(conthot / 500, 2))) + "\n"
output += "Percent of posts in New and Controversial: {}%".format(str(round(newcont / 500, 2))) + "\n"

output += "\n" + "-----Time Between Posts-----" + "\n"

added = 0
posts = []
previous = ""
current = ""

for post in new:
    posts.append(post)
    if previous == "":
        previous = post
    else:
        current = post
        time = abs(current.created - previous.created)
        added += time
        previous = current
        current = ""

averaged = added / (len(posts) - 1)

minutes = averaged // 60
seconds = averaged % 60
seconds = round(seconds, 2)
hours = int(minutes // 60)
minutes = int(minutes % 60)
if len(str(minutes)) == 1:
    minutes = "0" + str(minutes)
if len(str(seconds).split('.')[0]) == 1:
    seconds = "0" + str(seconds)
if len(str(hours)) == 1:
    hours = "0" + str(hours)


averaged = str(hours) + ":" + str(minutes) + ":" + str(seconds)

output += "Average time between new posts: " + str(averaged) + "\n"

clear()

print(output)