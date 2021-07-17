import time
import pytz
import datetime
import json
import urllib.request
from timezonefinder import TimezoneFinder
tf = TimezoneFinder()


def utc_to_local(utc_dt, tz=None):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=tz)


def main():
    locationinput = input("Location: ")
    with urllib.request.urlopen("https://nominatim.openstreetmap.org/search/{}?format=json".format(locationinput)) as url:
        data = json.loads(url.read().decode())
    """if len(data) == 0:
        print("Invalid location")
        continue"""
    location = data[0]
    name = location['display_name']
    latitude, longitude = float(location['lat']), float(location['lon'])

    timezone = tf.timezone_at(lng=longitude, lat=latitude)
    dt = datetime.datetime.now(pytz.timezone(timezone))
    day = dt.strftime("%m/%d/%Y")
    time = dt.strftime("%H:%M:%S")
    zone = dt.strftime("%Z%z")
    print("Location: " + name)
    print("Day: " + day)
    print("Timezone: " + zone)
    print("Time: " + time)


while True:
    main()
