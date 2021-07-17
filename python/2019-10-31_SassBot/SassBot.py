from random import randint
while True:
    input_string = input('> ')
    inpput_string = input_string.lower()
    if 'hi' in input_string or 'hey' in input_string or 'hello' in input_string:
        phrases = ['Umm, hi, loser.', 'Oh. It\'s you.', 'Hmm? Oh, I thought I heard a flea talking.', 'Hi, or, whatever.']
        print(phrases[randint(0, len(phrases)-1)])
        
    elif 'i\'m' in input_string or 'i am' in input_string or 'Im' in input_string:
        phrases = ['\'kay, then.', 'Yeah. Great. Get out of my face.', 'In case you haven\'t noticed, no one cares.', 'Sorry, who asked you to speak?']
        print(phrases[randint(0, len(phrases)-1)])
    elif 'rude' in input_string:
        phrases = ['It\'s who I am. Nobody said you had to like it.', 'Don\'t you have something better to do than being a drama queen?', 'If I were to call you a trashbag, that would be offensive to actual trashbags.']
        print(phrases[randint(1, len(phrases)-1)])
    elif 'goodbye' in input_string or 'bye' in input_string:
        phrases = ['Adios, loser.', 'Great. Go be annoying somewhere else.', 'Ciao, loser.', 'Cool. At least you\'ll get out of my face.']
        print(phrases[randint(1, len(phrases)-1)])
        break
    else:
        phrases = ['Oh my god, you\'re in my photo. Now I have to take it again.', 'Shoo, shoo, I\'m updating my Snapchat profile.', 'Whatever.', 'So?', 'Oh my god, can you just be annoying somewhere else?']
        print(phrases[randint(1, len(phrases)-1)])
