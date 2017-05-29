import requests
import json

def checkIsAlive(url):
    print(url)
    page = False
    try:
        page = requests.get(url, allow_redirects=False)
    except Exception as e:
        print('Website doesn\'t exists', e)

def main():
    with open("world_universities_and_domains.json") as JsonData:
        universities = json.load(JsonData)
        for university in universities[:]:
            checkIsAlive(university['web_page'])

if __name__ == '__main__':
    main()
