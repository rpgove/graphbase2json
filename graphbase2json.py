#!/usr/bin/env python

"""
Parses Stanford GraphBase .dat files and creates a .json file, a JSON
graph representation of .dat file suitable for loading in D3.js.
"""

import re
import json
import argparse

__author__ = "Robert Gove"
__license__ = "CC0 1.0 https://creativecommons.org/publicdomain/zero/1.0/"

parser = argparse.ArgumentParser(description="Convert a Stanford GraphBase .dat file to JSON")
parser.add_argument("--input", required=True, type=argparse.FileType('r'), help="Stanford GraphBase .dat file to read")
parser.add_argument("--output", required=True, type=argparse.FileType('w'), help="JSON file to store the result")

args = parser.parse_args()

lines = args.input.readlines()

# Test lines the define characters
char_re = re.compile('^[A-Z][A-Z]')

# Test lines that define encounters within chapters
chapter_re = re.compile('^[0-9]+\.[0-9]+\.[0-9]+')

# Maps node ID to node object:
# - id: Character ID
# - name: Character name,
# - chapters: List of chapters where this character had an encounter
nodes = {}

# - source: Character ID of source
# - target: Character ID of target
# - chapters: List of chapters where the source and target encountered each other
edges = {}

for line in lines:
	line = line.strip()

	if re.search(char_re, line):
		char_id = line[:2]
		char_name = line[line.find(' ')+1:line.find(',')]
		nodes[char_id] = { 'id': char_id, 'name': char_name, 'chapters': [] }

	elif re.search(chapter_re, line):
		# Skip lines that do not define encounters
		if line.find(':') == -1:
			continue

		chapter,encounters = line.split(':')

		# Update chapter list for each character
		for char_id in list(set(re.split(',|;', encounters))):
			nodes[char_id]['chapters'].append(chapter)
			nodes[char_id]['chapters'] = list(set(nodes[char_id]['chapters']))

		for enc in encounters.split(';'):
			char_ids = enc.split(',')

			if len(char_ids) < 2:
				continue

			for i in range(len(char_ids)):
				for j in range(i+1, len(char_ids)):
					node_ids = sorted([char_ids[i], char_ids[j]])
					edge_id = '-'.join(node_ids)
					if edge_id in edges:
						edges[edge_id]['chapters'].append(chapter)
						edges[edge_id]['chapters'] = list(set(edges[edge_id]['chapters']))
					else:
						edges[edge_id] = { 'source': node_ids[0], 'target': node_ids[1], 'chapters': [chapter] }

json.dump({'nodes': nodes.values(), 'links': edges.values()}, args.output)