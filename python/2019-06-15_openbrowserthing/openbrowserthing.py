import webbrowser

url = "https://www.youtube.com/watch?v=qNKtrZFbZno"


for i in range(1):
    browser = webbrowser.get('chrome')
    browser.open_new(url)