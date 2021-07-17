import urllib

import re
import pafy

video_search = raw_input(">")

video_search.replace(' ', '_')

query_string = urllib.urlencode({"search_query" : video_search})
print(query_string)
html_content = urllib.urlopen("http://www.youtube.com/results?" + query_string)
print(html_content)
search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
print(search_results)
print("http://www.youtube.com/watch?v=" + search_results[0])
