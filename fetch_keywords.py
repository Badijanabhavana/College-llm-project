import urllib.request
import re

try:
    req = urllib.request.Request('https://jntugvcev.edu.in/static/js/main.89808231.js', headers={'User-Agent': 'Mozilla/5.0'})
    text = urllib.request.urlopen(req).read().decode('utf-8')
    # Let's extract any string containing "Vice" or "Registrar" or "Principal" and some text around it.
    matches = re.findall(r'.{0,30}Vice[^\"]{0,50}', text, re.IGNORECASE)
    print("Vice:", set(matches))
    matches = re.findall(r'.{0,30}Registrar[^\"]{0,50}', text, re.IGNORECASE)
    print("Registrar:", set(matches))
    matches = re.findall(r'.{0,30}Principal[^\"]{0,50}', text, re.IGNORECASE)
    print("Principal:", set(matches))
except Exception as e:
    print(e)
