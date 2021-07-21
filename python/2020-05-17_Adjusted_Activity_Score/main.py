import praw
import operator
import csv
import os

file = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "2020-05-15.csv")

print("Opening data...")
with open(file, "r", encoding='ISO-8859-1') as f:
    csv_reader = csv.reader(f, delimiter=',')
    print("Reading data...")
    rows = [r for r in list(csv_reader)[1:]]
    rows = [{"real_name": row[0], "desc": row[1],
             "created_date": row[2], "subs": row[3]} for row in rows]

print("Initializing sorted list...")
sorteddict = {row["real_name"]: 0 for row in rows}

print("Sorting subreddits - most subscribers...")
subs = {}
