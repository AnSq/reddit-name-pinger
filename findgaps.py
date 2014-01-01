#!/usr/bin/python
import os
import convert

path_available = "data/available"
path_taken = "data/taken"
path_failed = "data/failed"

file_out_available = "data/merged_available.txt"
file_out_taken = "data/merged_taken.txt"
file_out_failed = "data/merged_failed.txt"

def main():
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
		available = list(set(available))
		available.sort()
		write_list(available, file_out_available)

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
		taken = list(set(taken))
		taken.sort()
		write_list(taken, file_out_taken)

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
		failed = list(set(failed))
		failed.sort()
		write_list(failed, file_out_failed)

	all = available + taken + failed
	all = list(set(all))
	all.sort(key=convert.to_num)

	print "\n===================\n"
	print "Available: %d" % len(available)
	print "Taken:     %d" % len(taken)
	print "Failed:    %d" % len(failed)
	print "Sum:       %d" % len(all)
	print "Total:     %d" % pow(38,4)
	print "Progress:  %.2f%%" % (100.0 * ((len(all) + 0.0) / pow(38,4)))
	print "\n===================\n"

	gaps = open("gaps.txt", "w")
	for i in range(0, len(all) - 1):
		curr = convert.to_num(all[i])
		next = convert.to_num(all[i+1])
		if next != curr + 1:
			str = "%s %s\n" % (convert.after(all[i]), all[i+1])
			print str,
			gaps.write(str)
	gaps.close()


def write_list(list, fname):
	file = open (fname, "w")
	for item in list:
		file.write(item + "\n")
	file.close()


if __name__ == "__main__":
	main()
