#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

# create lists of keys and values for the bar graph
top_items = sorted(items[:10], key=lambda item: item[1], reverse=False)
keys = [item[0] for item in top_items]
values = [item[1] for item in top_items]

# plot the bar graph
plt.bar(keys, values)

# set the title and axis labels
if args.input_path[-1] == 'g':
    plt.title('Use of ' + args.key.capitalize() + ' on Twitter in 2020 by Language')
    plt.xlabel('Language')
else:
    plt.title('Use of ' + args.key.capitalize() + ' on Twitter in 2020 by Country')
    plt.xlabel('Country')
if args.percent:
    plt.ylabel('Percent of Total')
else:
    plt.ylabel('Count')

# save the bar graph as a PNG file
if args.input_path[-1] == 'g':
    plt.savefig(args.key[1:] + '_lang.png')
else:
    plt.savefig(args.key[1:] + '_country.png')
