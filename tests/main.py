import json
import requests

import validate_json

def check_is_alive(url):
    """ check url then if url isn't alive, add to file """
    print(url)
    try:
        requests.get(url, allow_redirects=False, timeout=10.0)
    except requests.exceptions.ConnectionError as exc:
        print('- Website doesn\'t exists: ', exc)
        with open('result_test.txt', 'a') as result_test:  # Appending urls
            result_test.write(url + '\n')


def main():
    with open('result_test.txt', 'w') as result_test:  # Creating result_test.txt file
        result_test.write('### Result Wrong Links\n')
    validate_json.check_json_is_valid()
    with open('../world_universities_and_domains.json') as json_raw:
        universities = json.load(json_raw)
        for university in universities[:]:
            # TODO: Test all web pages
            check_is_alive(university['web_pages'][0])


if __name__ == '__main__':
    main()
