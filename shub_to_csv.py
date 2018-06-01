from pathlib import Path
import argparse
import jsonlines
import csv


def jsonl2csv(filepath, type_=None, include=None, exclude=None):
    def valid_type(item):
        if type_:
            return item.get('_type') == type_
        return True

    with jsonlines.open(filepath) as reader:

        while True:
            first = reader.read()
            if valid_type(first):
                break

        all_headers = set(first.keys())
        headers = set(include) if include else all_headers
        assert headers.issubset(all_headers)
        if exclude:
            exclude = set(exclude)
            assert exclude.issubset(all_headers)
            headers -= set(exclude)

        import ipdb; ipdb.set_trace()
        with Path(Path(filepath).with_suffix('.csv').name).open('w') as f:
            writer = csv.DictWriter(f, extrasaction='ignore', fieldnames=headers)
            writer.writeheader()
            writer.writerow(first)
            for obj in reader:
                if not valid_type(obj):
                    continue
                writer.writerow(obj)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('--exclude', help='Headers to include. Default to none', nargs='*')
    parser.add_argument('--include', help='Headers to include. Default to all', nargs='*')
    parser.add_argument('--type', help='Limit item to type')
    args = parser.parse_args()
    jsonl2csv(args.infile, args.type, args.include, args.exclude)

if __name__ == '__main__':
    main()