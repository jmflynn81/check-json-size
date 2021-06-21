import json
import argparse
from typing import Optional
from typing import Sequence
from typing import Union


def get_policy_size(pydict: str, start_key: list=None) -> int:
    if start_key is not None:
        for key in start_key:
            try:
                pydict = pydict[key]
            except KeyError:
                print(f'Key "{key}" does not exist in the JSON document')
                return None
    json_compact=json.dumps(pydict).replace(" ","")
    return len(json_compact)


def get_json(filename:str) -> dict:
    with open(filename) as f:
        json_string = f.read()
    return json.loads(json_string)


def parse_to_list(start_key:str) -> list:
    if start_key is not None:
        start_key = start_key.lstrip(".").rstrip(".")
        return start_key.split(".")
    else:
        return start_key


def string_to_int(max_size:str) -> Union[int, str]:
    try:    
        return int(max_size)
    except ValueError:
        return max_size


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start-key',
        type=parse_to_list,
        dest='start_key',
        default=None,
        help=('Starting key position if not the root of the document. This does'
              ' not support integer references for arrays, it currently only'
              ' works for object keys. Specified in jq notation, eg :-'
              ' .first_key.second_key.third_key'),
    )
    parser.add_argument(
        '--max-size',
        type=string_to_int,
        dest='max_size',
        default="6144",
        help=('Maximum document size. Default configured for IAM policies which'
              ' is currently 6144'),
    )
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    status = 0

    if type(args.max_size) is not int:
        print('Max size must be an integer number')
        return 1
    
    for filename in args.filenames:
        try:
            pydict = get_json(filename)
        except ValueError:
            print(f'Input File {filename} is not a valid JSON document')
            return 1
        
        policy_size = get_policy_size(pydict, args.start_key)
        
        if policy_size is None:
            return 1
        
        if policy_size > args.max_size:
            print(f'{filename}: JSON object size of {policy_size} characters is'
                  f' greater than the specified maximum of {args.max_size}'
                  f' characters')
            status = 1
    
    return status


if __name__ == '__main__':
    exit(main())
