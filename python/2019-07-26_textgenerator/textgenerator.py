import praw

reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]',
                     username='[REDACTED]',
                     password='[REDACTED]')

text = ""

subreddit = reddit.subreddit("entitledparents")

print("getting text")

for submission in subreddit.top(limit=100):
    text = text + submission.selftext
    text = text + "\n\n$!!$\n\n"


print("writing")
with open("/media/trig/5B55-6159/textgenerator/text.txt", "w") as training:
    text = text.replace("\n", "")
    text = text.replace("$!!$", "\n")
    training.write(text)

print("training")
from textgenrnn import textgenrnn

textgen = textgenrnn() 
textgen.train_from_file("/media/trig/5B55-6159/textgenerator/text.txt")
textgen.generate()