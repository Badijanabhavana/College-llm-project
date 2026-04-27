import urllib.request
import json
import re

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        return urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    except Exception as e:
        return f"ERROR: {e}"

# Fetch notifications
notifs = fetch("https://api.jntugvcev.edu.in/api/updates/allnotifications")
print("=== NOTIFICATIONS ===")
try:
    data = json.loads(notifs)
    for item in data[:20]:
        print(item)
except:
    print(notifs[:3000])

print()
