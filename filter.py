import json
import os
import string
import sys


def _country_filter(src, scope, out):
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


def country_filter(src, scopes):
    """
    Either make multiple data searches or
    execute one. {NEEDS IMPROVEMENT, O(kN) => O(n)}

    :arg src: source dictionary
    :arg scopes: source selectors
    """
    out = []

    if type(scopes) is list:
        [out.extend(_country_filter(src, scope, out)) for scope in scopes]
    else:
        out = _country_filter(src, scopes, out)

    return out


def main():
    args = []
    temp_arg = ""
    first_word = True

    # Retrieve our selecting countries (seperated by commas)
    for arg in sys.argv[1:]:
        temp_arg += arg if first_word else " " + arg
        first_word = False

        if arg[-1] == ",":
            args.append(temp_arg[:-1])
            temp_arg = ""
            first_word = True

    if temp_arg:
        args.append(temp_arg)

    if not args:
        return

    # Load the source
    src = None
    with open("./world_universities_and_domains.json") as src_file:
        src = json.load(src_file)

    if src is None:
        return

    # Write the filtered result
    with open("./filtered_world_universities_and_domains.json", "w") as dest_file:
        json.dump(country_filter(src, args), dest_file)


if __name__ == "__main__":
    main()
