import json
import os
import string
import sys


def country_filter(src, scope):
    """
    Search the data for a single country

    :arg src: source dictionary
    :arg scope: source selector
    """

    def filter(entry, item):
        matching = entry["country"]

        if item == matching or item == matching.lower() or item == matching.upper():
            return True

        else:
            return False

    return [entry for entry in src if filter(entry, scope)]


def main():
    args = []
    

    # Retrieve our selecting countries (seperated by commas)
    for arg in sys.argv[1:]:
        args.append(arg)

    if not args:
        print("No arguments provided to filter")
        return
    
    # Load the source
    try:
        with open("./world_universities_and_domains.json") as src_file:
            src = json.load(src_file)
    except:
        print("The JSON file doesn't exist")
        return
    

    # Write the filtered result
    for arg in args:

        with open("./{}_filtered_world_universities_and_domains.json".format(arg), "w") as dest_file:
            json.dump(country_filter(src, arg), dest_file)


if __name__ == "__main__":
    main()
