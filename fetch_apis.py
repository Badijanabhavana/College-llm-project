import urllib.request
import re

try:
    req = urllib.request.Request('https://jntugvcev.edu.in/static/js/main.89808231.js', headers={'User-Agent': 'Mozilla/5.0'})
    text = urllib.request.urlopen(req).read().decode('utf-8')
    # Find all API endpoints ending in .json or starting with https://api.jntugvcev.edu.in
    matches = re.findall(r'https://[^\s\"\'\>]+', text)
    apis = set(m for m in matches if 'api' in m or 'json' in m)
    print(apis)
except Exception as e:
    print(e)
