import urllib.request
import re

try:
    req = urllib.request.Request('https://jntugvcev.edu.in/static/js/main.89808231.js', headers={'User-Agent': 'Mozilla/5.0'})
    text = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'Prof\.\s[A-Za-z\s\.]+', text)
    print(set(matches))
except Exception as e:
    print(e)
