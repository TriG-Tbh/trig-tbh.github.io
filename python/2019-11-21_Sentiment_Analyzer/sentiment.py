import textblob
import os

def get_textblob(text):
    obj = textblob.TextBlob(text)
    return obj

def parse_polarity(polarity):
    if polarity > 0.0:
        polarity = "Positive"
    elif polarity == 0.0:
        polarity = "Neutral"
    elif polarity < 0.0:
        polarity = "Negative"
    return polarity

def sentimentality(text):
    values = {}
    values["text"] = text
    blob = get_textblob(text)
    sentiment = blob.sentiment.polarity
    values["value"] = sentiment
    sentiment = parse_polarity(sentiment)
    values["sentiment"] = sentiment
    return values

if __name__ == "__main__":
    while True:
        os.system("clear")
        message = input("Enter message: ")
        os.system("clear")
        values = sentimentality(message)
        print("Input message: {}\nSentiment: {} ({})".format(values["text"], values["sentiment"], round(values["value"], 2)))
        input("Press enter to continue. ")