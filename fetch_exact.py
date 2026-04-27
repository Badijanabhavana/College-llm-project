import urllib.request
import re

try:
    req = urllib.request.Request('https://jntugvcev.edu.in/static/js/main.89808231.js', headers={'User-Agent': 'Mozilla/5.0'})
    text = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'.{0,100}role:"Hon\\u2019ble Vice-Chancellor".{0,100}', text, re.IGNORECASE)
    for m in matches:
        print("VC MATCH:", m)
        
    matches = re.findall(r'.{0,100}role:"Registrar i/c".{0,100}', text, re.IGNORECASE)
    for m in matches:
        print("REG MATCH:", m)
except Exception as e:
    print(e)
