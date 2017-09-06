import json

def check_json_is_valid():
    try:
        with open("../world_universities_and_domains.json") as json_file:
            json.load(json_file)
    except ValueError:
        print("JSON is not valid")
