""" Testing All University Links """
import json
import requests


def check_is_alive(url):
    """ request url then controlling is alive """
    print(url)
    try:
        requests.get(url, allow_redirects=False, timeout=10.0)
    except requests.exceptions.ConnectionError as exc:
        print('- Website doesn\'t exists: ', exc)


def main():
    with open('world_universities_and_domains.json') as json_raw:
        universities = json.load(json_raw)
        for university in universities[:]:
            check_is_alive(university['web_page'])


if __name__ == '__main__':
    main()
