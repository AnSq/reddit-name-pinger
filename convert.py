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
		print diff_hours(sys.argv[1], sys.argv[2])


def diff_days(start, end):
	return (to_num(end) - to_num(start)) / 43200.0


def diff_hours(start, end):
	return (to_num(end) - to_num(start)) / 1800.0


def percent_complete(start, end, current):
	range = to_num(end) - to_num(start)
	pos = to_num(current) - to_num(start)
	return 100.0 * pos / range


def from_num(n):
	digits = []
	name = ""
	while n > 0:
		digits.insert(0, n % len(chars))
		n //= len(chars)
	for d in digits:
		name += chars[d]
	return name


def pad(name, l):
	n = name
	while len(n) < l:
		n = chars[0] + n
	return n


def after(name):
	result = from_num(1 + to_num(name))
	if len(result) == len(name):
		return pad(result, len(name))
	else:
		return chars[0] * (len(name) + 1)


def before(name):
	if to_num(name) == 0:
		return chars[len(chars)-1] * (len(name) - 1)
	else:
		return pad(from_num(-1 + to_num(name)), len(name))


if __name__ == "__main__":
	main()
