import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        return urllib.request.urlopen(req, timeout=15).read().decode('utf-8')
    except Exception as e:
        return f"ERROR: {e}"

text = fetch("https://jntugvcev.edu.in/static/js/main.89808231.js")

portals = re.findall(r'href:"(https?://[^"]+)"', text)
unique_portals = sorted(set(portals))
print("=== PORTALS / EXTERNAL LINKS ===")
for p in unique_portals:
    print(p)
