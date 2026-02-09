import time
import requests

URL = "http://127.0.0.1:8000/api/active-tags"

while True:
    print(requests.get(URL).json())
    time.sleep(1)