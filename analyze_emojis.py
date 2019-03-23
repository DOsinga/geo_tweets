#!/usr/bin/env python
import argparse
import glob
import json
import os
import random
import shutil
from collections import Counter, defaultdict
import datetime
from csv import DictWriter

import emoji
import tqdm

from split_by_emoji import TIME_SLICE_SECONDS

SLICES_PER_DAY = 3600 * 24 // TIME_SLICE_SECONDS
EMOJIS_PER_DAY = 1500


def find_unbalanced(xy_ch, unbalanced_out):
    emojis = defaultdict(Counter)
    for ch, lst in xy_ch.items():
        for ts, x, y in lst:
            ts = int(ts) / 1000 + x  * 12
            utc_ts = datetime.datetime.utcfromtimestamp(ts)
            emojis[''][utc_ts.hour] += 1
            emojis[ch][utc_ts.hour] += 1
    relative = {}
    c = Counter({t[0]: sum(t[1]) for t in emojis.items()})
    rec_all = emojis['']
    for k, v in c.most_common(1200):
        if k:
            relative[k] = [emojis[k][h] / rec_all[h] for h in rec_all.keys()]
            ss = sum(relative[k])
            relative[k] = [c / ss for c in relative[k]]
    unbalanced = {}
    for k, v in relative.items():
        v = list(sorted(v))
        if v[0] + v[1] == 0:
            print(k, v)
        else:
            unbalanced[k] = (v[-1] + v[-2]) / (v[0] + v[1])

    with open(unbalanced_out, 'w', encoding='utf8') as fout:
        for k, v in sorted(unbalanced.items(), key=lambda t: t[1], reverse=True):
            print(k, v)
            if v > 3:
                name = emoji.UNICODE_EMOJI[k].replace(':', '')
                fout.write('%s:%s:%s\n' % (name, k, v))


def geo_hash(x, y):
    # For now return a grid cell:
    return int(x // 100) + 36 * int(y // 100)


def process_emojis(input, output_folder, by_hour_fn, unbalanced):
    with open(input) as fin:
        xy_ch = json.load(fin)

    find_unbalanced(xy_ch, unbalanced)

    by_hour = defaultdict(lambda: [0 for _ in range(24)])
    by_hash = Counter()
    for ch, lst in xy_ch.items():
        for ts, x, y in lst:
            by_hash[geo_hash(x, y)] += 1

    emojis = defaultdict(lambda: [[] for _ in range(SLICES_PER_DAY)])
    for ch, lst in xy_ch.items():
        if len(lst) < EMOJIS_PER_DAY * 2:
            print(f'skipping {ch}, has only {len(lst)} items')
            continue
        weighted = []
        for ts, x, y in lst:
            hour = int((ts * TIME_SLICE_SECONDS) / 3600 - (x / 30) + 24) % 24
            by_hour[ch][hour] += 1
            weighted.append((random.random() / max(by_hash[geo_hash(x, y)], 5),
                            ts, x, y))
        for _, ts, x, y in sorted(weighted, reverse=True)[:EMOJIS_PER_DAY]:
            emojis[ch][ts].append((x, y))

    with open(by_hour_fn, 'w') as fout:
        writer = DictWriter(fout, ['name', 'emoji'] + [h for h in range(24)])
        writer.writeheader()
        for ch, lst in by_hour.items():
            writer.writerow({'name': emoji.UNICODE_EMOJI[ch].replace(':', ''),
                             'emoji': ch,
                             **{h: lst[h] for h in range(24)}})

    os.makedirs(output_folder, exist_ok=True)
    for e, ll in emojis.items():
        fn = emoji.UNICODE_EMOJI[e][1:-1]
        pngs = glob.glob('/Users/douwe/checkout/noto-emoji/png/128/emoji_u%04x*.png' % ord(e))
        if not pngs:
            print(fn, 'missing')
            continue
        shutil.copyfile(
            pngs[0],
            os.path.join(output_folder, fn + '.png')
        )
        with open(os.path.join(output_folder, fn + '.json'), 'w', encoding='utf8') as fout:
            js = {'emoji': e,
                  'name': emoji.UNICODE_EMOJI[e],
                  'img': fn + '.png',
                  'timestamps': ll}
            json.dump(js, fout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='split_emojis.json')
    parser.add_argument('--by_hour', type=str, default='by_hour.csv')
    parser.add_argument('--output_dir', type=str, default='by_emoji')
    parser.add_argument('--unbalanced', type=str, default='unbalanced.txt')
    args = parser.parse_args()

    process_emojis(args.input, args.output_dir, args.by_hour, args.unbalanced)
