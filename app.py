import json
from collections import defaultdict
from flask import Flask, request
from pytrie import Trie
import uuid

app = Flask(__name__)

data = list()
country_index = defaultdict(list)
name_index = dict()

@app.route("/search")
def search():
    if not data_loaded:
        load_data()

    country = request.args.get('country')
    name = request.args.get('name')
    filtered = data

    if name and country:
        name = name.lower()
        country = country.lower()
        name_filtered = prefix_tree.values(prefix=name)
        country_filtered = country_index[country]
        filtered = [i for i in name_filtered if i['name'] in [_i['name'] for _i in country_filtered]]

    elif name:
        name = name.lower()
        filtered = prefix_tree.values(prefix=name)
    elif country:
        country = country.lower()
        filtered = country_index[country]

    return json.dumps(filtered)

data_loaded = False

def load_data():
    global data_loaded, prefix_tree, data, country_index, name_index
    json_data=open("world_universities_and_domains.json").read()
    data = json.loads(json_data)
    for i in data:
        country_index[i["country"].lower()].append(i)
        name_index[i['name'].lower()] = i
        for splitted_name in i['name'].split(' '):
            name_index[splitted_name.lower() + str(uuid.uuid1())] = i
    prefix_tree = Trie(**name_index)

    data_loaded = True


@app.route('/')
def index():

    if not data_loaded:
        load_data()

    data = {'author': {'name': 'hipo', 'website': 'http://hipolabs.com'},
            'example': 'http://universities.hipolabs.com/search?name=middle&country=Turkey',
            'github': 'https://github.com/Hipo/university-domains-list'}
    return json.dumps(data)

if __name__ == "__main__":
    app.run(debug=True)
