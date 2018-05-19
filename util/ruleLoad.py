#!/usr/bin/env python
# __Autehor__:cmustard

import json


def load(path):
	with open(path, "r") as f:
		raw_rule_dicts = json.load(f)

	return raw_rule_dicts




if __name__ == '__main__':
	print(load(r"..\fingerprint\test.json"))
