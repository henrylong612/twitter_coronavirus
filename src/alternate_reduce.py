#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths',nargs='+',required=True)
parser.add_argument('--output_path',required=True)
parser.add_argument('--keys',nargs='+',required=True)
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# load each of the input paths
total = defaultdict(lambda: Counter())
for path in args.input_paths:
    with open(path) as f:
        tmp = json.load(f)
        filename = os.path.basename(path)
        date = filename[10:18]
        total[date] = tmp

new_dict = {}

for day in total.keys():
    for key in args.keys:
        if key not in new_dict:
            new_dict[key] = {}
        if day not in new_dict[key]:
            new_dict[key][day] = 0
        try:
            for lang in total[day][key].values():
                new_dict[key][day] += lang
        except KeyError:
            pass

for key in new_dict:
    days = sorted(new_dict[key].keys())
    values = [new_dict[key][day] for day in days]
    plt.plot(days, values, label=key)

# Add title and axis labels
plt.title('Tweet volume by day and hashtag')
plt.xlabel('Day')
plt.ylabel('Tweet count')

plt.savefig(args.output_path+'.png')
