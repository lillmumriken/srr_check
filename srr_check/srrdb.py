#!/usr/bin/env python3
import requests
from os import path, mkdir

apiurl = "https://www.srrdb.com/api"

def request(url):
    """ Make request and return json """

    r = requests.get(url)
    if r.status_code != 200:
        return False
    return r.json()

def search(relname):
    """ Get relase details from srrdb and return list of files """

    r = request(f"{apiurl}/search/r:{relname}")

    if r["resultsCount"] == "0":
        # implement fallback crc check
        return False

    relname = r["results"][0]["release"]

    r = request(f"{apiurl}/details/{relname}")
    return r

def download(relname, filename):
    """ Download file from srrdb """
    ext = path.splitext(filename)[-1]
    if ext not in [".jpg", ".nfo", ".sfv"]:
        return False
    # Extract first folder of the path (this would contain filename if no dir)
    folder = filename.split('/')[0]
    # Check that it's not a file and the path does not exist already
    if not '.' in folder and not path.exists(folder):
        mkdir(folder)
    url = f"https://www.srrdb.com/download/file/{relname}/{filename}"
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        return False
    open(filename, 'wb').write(r.content)
    return True

if __name__ == "__main__":
    path = ""
    relname = path.split("/")[-1]
    files = search(relname)
    print(files)
