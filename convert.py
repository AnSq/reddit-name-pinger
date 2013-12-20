#!/usr/bin/python
import string
import sys

table = {}
chars = string.ascii_lowercase + string.digits + "-_"


def init():
	for i in range(0, len(chars)):
		table[chars[i]] = i


def to_num(name):
	if len(table) == 0:
		init()
	total = 0
	for i in range(0, len(name)):
		total *= len(chars)
		total += table[name[i]]
	return total


def main():
	if len(sys.argv) == 2:
		print to_num(sys.argv[1])
	elif len(sys.argv) == 3:
		print diff_days(sys.argv[1], sys.argv[2])


def diff_days(start, end):
	return (to_num(end) - to_num(start)) / 43200.0


if __name__ == "__main__":
	main()
