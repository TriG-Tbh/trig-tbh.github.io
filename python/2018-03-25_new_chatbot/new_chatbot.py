from chatbot import *

chatbot = ChatBot(self, name, **kwargs)

class MyBot(chatbot.ChatBot):
	def __init__(self):
		import chatbot
		MyBot.__init__ (self)
		
if __name__ == '__main__':
	bot = MyBot()
	bot.start()
	
