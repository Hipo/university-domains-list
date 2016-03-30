import json
from collections import defaultdict
from flask import Flask, request
from pytrie import Trie

app = Flask(__name__)

data = list()
country_index = defaultdict(list)
name_index = dict()

@app.route("/search")
def search():
    country = request.args.get('country')
    name = request.args.get('name')
    filtered = data

    if name and country:
        name_filtered = prefix_tree.values(prefix=name)
        country_filtered = country_index[country]
        filtered = [i for i in name_filtered if i['name'] in [_i['name'] for _i in country_filtered]]

    elif name:
        filtered = prefix_tree.values(prefix=name)
    elif country:
        filtered = country_index[country]

    return json.dumps(filtered)

@app.route('/')
def index():
    data = {'author': {'name': 'hipo', 'website': 'http://hipolabs.com'},
            'example': 'http://universities.hipolabs.com/search?name=middle&country=Turkey',
            'github': 'https://github.com/Hipo/university-domains-list'}
    return json.dumps(data)

if __name__ == "__main__":
    json_data=open("world_universities_and_domains.json").read()
    data = json.loads(json_data)
    for i in data:
        country_index[i["country"]].append(i)
        name_index[i["name"]] = i
    prefix_tree = Trie(**name_index)
    app.run()
