import re
import atexit

import numpy
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import multiprocessing
import threading

url = input("> ")

urldata = urlparse(url)

domain = urldata.netloc
proto = urldata.scheme + "://"

data = {}

def save():
    global data
    with open("output.json", "w") as f:
        json.dump(data, f, indent=4)


def getData(*args):
    global data
    for a in args:
        if "http" in a:
            ur = a
        else:
            ur = proto + domain + a
        try:
            rr = requests.get(ur)

            data[ur] = {"status": rr.status_code}
            if rr.status_code == 200 and "text/html" in rr.headers['content-type']:
                print(ur)
                emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', rr.text))
                data[ur]["count"] = len(emails)
                data[ur]["emails"] = list(emails)
            rr.close()
        except Exception as e:
            print(ur, type(e), e)


atexit.register(save)


r = requests.get(url)
if r.status_code == 200:
    pars = BeautifulSoup(r.text, "html.parser")
    links = list(set(x["href"] for x in filter(lambda x: "href" in x.attrs, set(pars.find_all("a")))))
    cores = multiprocessing.cpu_count()

    tasks = [tuple(x) for x in numpy.array_split(links, cores)]
    processes = []

    for i, task in enumerate(tasks):
        processes.append(threading.Thread(target=getData, args=task))

    for p in processes:
        p.start()

    for p in processes:
        p.join()


save()

