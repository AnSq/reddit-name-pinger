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
	num_available = 0
	num_taken = 0
	num_failed = 0

	for fname in os.listdir(path_available):
		num_available += 1
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
		num_taken += 1
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
		num_failed += 1
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

	print "\n===================\n"

	s = len(available)
	s_available = set(available)
	print "%d duplicate names removed from available." % (s - len(s_available))

	s = len(taken)
	s_taken     = set(taken)
	print "%d duplicate names removed from taken." % (s - len(s_taken))

	s = len(failed)
	s_failed    = set(failed)
	print "%d duplicate names removed from failed." % (s - len(s_failed))

	s = len(s_available)
	s_available -= s_taken
	print "%d taken names removed from available." % (s - len(s_available))

	s = len(s_failed)
	s_failed    -= s_available
	print "%d available names removed from failed." % (s - len(s_failed))

	s = len(s_failed)
	s_failed    -= s_taken
	print "%d taken names removed from failed." % (s - len(s_failed))

	available = list(s_available)
	taken     = list(s_taken)
	failed    = list(s_failed)

	write_list(available, file_out_available)
	write_list(taken, file_out_taken)
	write_list(failed, file_out_failed)

	num_all = num_available + num_taken + num_failed
	all = available + taken + failed

	s = len(all)
	all = list(set(all))
	print "%d duplicate names removed from all (this should be 0)." % (s - len(all))

	all.sort(key=convert.to_num)

	print "\n===================\n"

	print "Available: %d \tin %d files" % (len(available), num_available)
	print "Taken:     %d \tin %d files" % (len(taken), num_taken)
	print "Failed:    %d \tin %d files" % (len(failed), num_failed)
	print "Sum:       %d \tin %d files" % (len(all), num_all)
	print "Total:     %d" % pow(38,4)
	print "Progress:  %.2f%%" % (100.0 * ((len(all) + 0.0) / pow(38,4)))

	print "\n===================\n"

	print "Gaps:"
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
