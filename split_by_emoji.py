#!/usr/bin/env python
import argparse
import json
import os
import random
import shutil
from collections import Counter, defaultdict
import glob
from csv import DictWriter

import emoji
import tqdm

TIME_SLICE_SECONDS = 120

def main(input, output_fn):
    """Split the input by emoji.

    For each write out a json document of the form:
       {'emoji': <>,
        'timestamps': [[(lat1, lng1), (lat2, lng2),...]]
    """
    count = 0
    xy_ch = defaultdict(list)
    for line in tqdm.tqdm(open(input, encoding='utf8')):
        count += 1
        ts, lat, lng, txt = line.split(',', 3)
        lat, lng = map(float, (lat, lng))
        ts = int(int(ts) / 1000) % (3600 * 24)
        ts //= TIME_SLICE_SECONDS
        for ch in {ch2 for ch2 in line if ch2 in emoji.UNICODE_EMOJI}:
            x = int((180 + lng) * 10)
            y = int((90 - lat) * 10)
            xy_ch[ch].append((ts, x, y))
    with open(output_fn, 'w') as fout:
        json.dump(xy_ch, fout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='tweets.txt')
    parser.add_argument('--output', type=str, default='split_emojis.json')
    args = parser.parse_args()

    main(args.input, args.output)
