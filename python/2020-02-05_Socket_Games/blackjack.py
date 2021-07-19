import random

deck = []

for s in "SDCH":
    for value in "234567890JQKA":
        card = s + value
        deck.append(card)

print("Shuffling...")

random.shuffle(deck)