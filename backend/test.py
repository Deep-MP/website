

import requests
def run():
    headers = {"Content-Type": "application/json;charset=utf-8"}
    url = "http://localhost:5000/get_data"
    res = requests.get(url, headers=headers)
    print(res.text)

def get_paperswithcode():
    headers = {"Content-Type": "application/json;charset=utf-8"}
    url = "http://localhost:5000/get_paperswithcode"
    res = requests.get(url, headers=headers)
    print(res.text)

def get_github():
    headers = {"Content-Type": "application/json;charset=utf-8"}
    url = "http://localhost:5000/get_github"
    res = requests.get(url, headers=headers)
    print(res.text)

def get_semantic():
    headers = {"Content-Type": "application/json;charset=utf-8"}
    url = "http://localhost:5000/get_semantic"
    res = requests.get(url, headers=headers)
    print(res.text)

if __name__ == "__main__":
    #run()
    #get_paperswithcode()
    get_github()
    #get_semantic()
