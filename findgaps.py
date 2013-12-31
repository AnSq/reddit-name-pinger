#!/usr/bin/python
import os

path_available = "data/available"
path_taken = "data/taken"
path_failed = "data/failed"

available = []
taken = []
failed = []
all = []

for fname in os.listdir(path_available):
	path = os.path.join(path_available, fname)
	print path
	s = set()
	file = open(path, "r")
	for line in file:
		name = line.strip()
		if not name in s:
			s.add(name)
			available.append(name)
	file.close()
	available.sort()

for fname in os.listdir(path_taken):
	path = os.path.join(path_taken, fname)
	print path
	s = set()
	file = open(path, "r")
	for line in file:
		name = line.strip()
		if not name in s:
			s.add(name)
			taken.append(name)
	file.close()
	taken.sort()

for fname in os.listdir(path_failed):
	path = os.path.join(path_failed, fname)
	print path
	s = set()
	file = open(path, "r")
	for line in file:
		name = line.split(":")[1].strip()
		if not name in s:
			s.add(name)
			failed.append(name)
	file.close()
	failed.sort()

all = available + taken + failed
all.sort()

print "\n===================\n"
print "Available: %d" % len(available)
print "Taken:     %d" % len(taken)
print "Failed:    %d" % len(failed)
print "Sum:       %d" % len(all)
print "Total:     %d" % pow(38,4)
print "Progress:  %.2f%%" % (100.0 * ((len(all) + 0.0) / pow(38,4)))
