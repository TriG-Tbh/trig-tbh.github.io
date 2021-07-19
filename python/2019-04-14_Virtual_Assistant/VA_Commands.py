def search(my_input):
	import wikipedia
	import wolframalpha

	app_id = "[REDACTED]"
	client = wolframalpha.Client(app_id)

	try:
		res = client.query(my_input)
		answer = ""
		answer = next(res.results).text
		if answer != "(no data available)":
			print("Response: \n" + answer)
		else:
			print("WRA returned no response, checking Wikipedia")
			try:
				print("Response: " + wikipedia.summary(my_input, sentences=2))
			except wikipedia.DisambiguationError as e:
				string = "\"" + my_input + "\" may refer to:" + "\n"
				for index, value in enumerate(e.options, 1):
					string = string + ("{}. {}".format(index, value) + "\n")
				print(string)
				article = input("Which of the above would you like a summary about? ")
				try:
					print("Response: " + wikipedia.summary(e.options[int(article) - 1], sentences=2))
				except:
					print("Please choose an option above.")
		
	except:
		try:
			print("Response: " + wikipedia.summary(my_input, sentences=2))
		except wikipedia.DisambiguationError as e:
			string = "\"" + my_input + "\" may refer to:" + "\n"
			for index, value in enumerate(e.options, 1):
				string = string + ("{}. {}".format(index, value) + "\n")
			print(string)
			article = input("Which of the above would you like a summary about? ")
			try:
				print("Response: " + wikipedia.summary(e.options[int(article) - 1], sentences=2))
			except:
					print("Please choose an option above.")
		
	print("")


def play(query, playvideo=False):
	import sys
	non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
	import pafy
	import vlc
	query = query.replace(' ', '_')
	import urllib.request
	import urllib.parse
	import re
	query_string = urllib.parse.urlencode({"search_query" : query})
	print('Searching...')
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	print('Finding videos...')
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	base = ("http://www.youtube.com/watch?v=" + search_results[0])
	video = pafy.new(base)
	print("Now playing \"" + video.title.translate(non_bmp_map) + "\", please wait")
	if playvideo == True:
       		bestvid = video.getbest()
	if playvideo == False:
		bestvid = video.getbestaudio()
	p = vlc.MediaPlayer(bestvid.url)
	p.play()

def stopplaying():
	try:
		p.stop()
		print("Stopping")
	except:
		print("Nothing is playing right now")

def pause():
	try:
		p.pause()
		print("Pausing")
	except:
		print("Nothing is playing right now")

def resume():
	try:
		p.play()
		print("Resuming")
	except:
		print("Nothing is playing right now")

def googlesearch(query):
	query = command.replace("!google ", "")
	from bs4 import BeautifulSoup
	from bs4 import BeautifulSoup as bs
	from googlesearch import search
	import urllib
	counter = 0
	fullurls = ""
	urls = []
	for url in search(query, stop=10):
		urls.append(url)
		counter += 1
		soup = bs(urllib.request.urlopen(url), "html.parser")
		fullurls += str(counter) + ". " + soup.title.string + " (" + url + ")\n"
	print(fullurls)
	website = input("Enter which number website you want to find: ")
	import requests
	import re
	html = requests.get(urls[int(website) - 1]).content
	unicode_str = html.decode("utf8")
	encoded_str = unicode_str.encode("ascii",'ignore')
	news_soup = BeautifulSoup(encoded_str, "html.parser")
	a_text = news_soup.find_all('p')
	y = [re.sub(r'<.+?>',r'',str(a)) for a in a_text]
	fullstring = ""
	for text in y:
		fullstring += text
	print(fullstring)

def evaluate(query):
	import sys
	non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
	query = str(query)
	import wolframalpha
	app_id = "[REDACTED]"
	client = wolframalpha.Client(app_id)
	try:
		answer = eval(query)
		print("Response: " + str(answer))
	except:
		'''try:'''
		res = client.query(query)
		answer = ""
		for pod in res.pods:
			for sub in pod.subpods:
				answer = answer + str(sub.text.translate(non_bmp_map)) + "\n"
		print("Response: " + str(answer))
		if answer != "(no data available)":
			print("Response: \n" + str(answer))
		'''	else:
					print("\"" + query + "\" cannot be evaluated")
		except:
			print("\"" + query + "\" cannot be evaluated")'''

def wolframalpha(question):
	import sys
	non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
	question = str(question)
	import wolframalpha
	app_id = "[REDACTED]"
	client = wolframalpha.Client(app_id)
	res = client.query(question)
	answer = ""
	print(next(res.results).text)
	print(answer)
