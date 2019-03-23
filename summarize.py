#!/usr/bin/env python
from __future__ import print_function

import argparse
import json


def main(input, output):
    lines = 0
    with open(output, 'w', encoding='utf8') as fout:
        for line in open(input):
            rec = json.loads(line)
            lng, lat = rec['coordinates']['coordinates']
            txt = ' '.join(rec['text'].splitlines())
            lines += 1
            if lines % 10000 == 0:
                print(lines, txt)
            fout.write('%s,%s,%s,%s\n' % (rec['timestamp_ms'], lat, lng, txt))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='.twitter_cache')
    parser.add_argument('--output', type=str, default='tweets.txt')
    args = parser.parse_args()

    main(args.input, args.output)
