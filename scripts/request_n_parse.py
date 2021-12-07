import os
import requests
from bs4 import BeautifulSoup

def read_url(url, ext='', params={}):
    response = requests.get(url, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    directories = [url + node.get('href') for node in soup.find_all('a') 
              if '?' not in node.get('href')
              and node.get('href') != "/"]
    return directories
    

urls = ["https://activebrainatlas.ucsd.edu/data/", "https://lightsheetatlas.pni.princeton.edu/public/"]
for url in urls:
    print(url)
    directories = read_url(url) 
    for directory in directories:
        layer_name = os.path.basename(os.path.normpath(directory))
        print(layer_name)
    print()
