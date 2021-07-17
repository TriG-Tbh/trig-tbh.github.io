import requests
r =requests.get('https://api.thingspeak.com/apps/thinghttp/send_request?api_key=[REDACTED]')
print r.text
