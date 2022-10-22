import requests
from bs4 import BeautifulSoup
import json

urls = []

while True:
    i = input("> ")
    if i == "":
        break
    urls.append(i)

data = {}

for url in urls:
    r = requests.get(url)
    if r.status_code == 200:
        pars = BeautifulSoup(r.text, "html.parser")
        count = 0
        for a in pars.find_all("a"):
            if "href" in a.attrs:
                count += 1
        data[url] = count
    else:
        data[url] = -r.status_code

with open("output.json", "w") as f:
    json.dump(data, f, indent=4)
