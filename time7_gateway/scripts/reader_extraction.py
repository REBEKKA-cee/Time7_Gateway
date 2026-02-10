import json
import requests

URL = "http://127.0.0.1:8000/api/active-tags"


with requests.get(URL, stream=True) as r:
    r.raise_for_status()
    for line in r.iter_lines(decode_unicode=True):
        if not line:
            continue
        print(line) 