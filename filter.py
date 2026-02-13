import json
import os
import string
import sys


def _country_filter(src, scope, out):
    """
    Search the data for a single country

    :arg src: source dictionary
    :arg scope: source selector
    :arg out: unused parameter (kept for compatibility)
    """

    def filter_entry(entry, item):
        matching = entry["country"]
        return item.lower() == matching.lower()

    return [entry for entry in src if filter_entry(entry, scope)]


def country_filter(src, scopes):
    """
    Filter data by country(ies) with improved efficiency and no duplicates

    :arg src: source dictionary
    :arg scopes: source selectors (string or list)
    """
    if not scopes:  # Handle empty scopes
        return src

    if isinstance(scopes, str):
        return _country_filter(src, scopes, None)

    if isinstance(scopes, list):
        if not scopes:  # Empty list
            return src

        # Convert all scopes to lowercase for case-insensitive comparison
        normalized_scopes = [scope.lower() for scope in scopes]

        # Filter entries where country matches any scope (case-insensitive)
        filtered_entries = [
            entry for entry in src if entry["country"].lower() in normalized_scopes
        ]

        # Sort by country name for consistent ordering
        return sorted(filtered_entries, key=lambda x: x["country"])

    return []


def main():
    args = []
    temp_arg = ""
    first_word = True

    # Retrieve our selecting countries (separated by commas)
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
