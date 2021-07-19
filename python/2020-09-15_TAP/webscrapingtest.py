import urllib.request
import requests
from bs4 import BeautifulSoup
from msal import PublicClientApplication as pca
import webbrowser


headers = {
    "Authorization": "no"
}

teamid = "[REDACTED]"

x = requests.get(f"https://graph.microsoft.com/beta/education/classes/{teamid}/assignments", headers=headers)

print(x.content)
