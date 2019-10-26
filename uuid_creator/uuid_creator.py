#!/usr/bin/env python3
import sys
import argparse
import uuid
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str,
                        help="Input file (JSON)")
    parser.add_argument("output_file", type=str,
                        help="Output file (JSON)")

    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as in_file:
        json_data = json.load(in_file)
        
        for school in json_data:
            uuid_parsed = school.get('uuid', None)
            if uuid_parsed != None:
                school['uuid'] = uuid.uuid4().__str__()
        
        with open(args.output_file, 'w', encoding='utf-8') as out_file:
            json.dump(json_data, out_file)