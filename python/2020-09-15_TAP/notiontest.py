from notion.client import NotionClient
from datetime import datetime

client = NotionClient(token_v2="[REDACTED]")

url = "https://www.notion.so/[REDACTED]?v=[REDACTED]"

board = client.get_collection_view(url)

page = client.get_block(url)

cv = client.get_collection_view(url)

row = cv.collection.add_row()
row.title = "Example Homework"
row.status = "Not started"
row.due_date = datetime.now()
row.class_ = "Example class name 2"
print("Done")