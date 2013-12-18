#!/usr/bin/python
import string
import requests
import time
import sys

chars = string.ascii_lowercase + string.digits + "-_"
agent = "name pinger 1.0 by /u/AnSq"
headers = {"User-Agent": agent}
file_available = open("reddit_available_names.txt", "a")
file_taken = open("reddit_taken_names.txt", "a")
file_fail = open("reddit_failed_names.txt", "a")
start_at = sys.argv[1]

started = False
num = 0

for a in range(0,len(chars)):
	A = chars[a]
	for b in range(0,len(chars)):
		B = chars[b]
		for c in range(0,len(chars)):
			C = chars[c]
			for d in range(0,len(chars)):
				D = chars[d]
				username = A + B + C + D
				if username == start_at:
					started = True
				if started:
					r = requests.head("http://www.reddit.com/user/" + username + "/.json", headers=headers)
					if r.status_code == 200:
						print "#  " + username
					elif r.status_code == 404:
						print "   " + username
					else:
						print "-  " + username + " " + str(r.status_code)

					if r.status_code == 200:
						file_taken.write(username + "\n")
					elif r.status_code == 404:
						file_available.write(username + "\n")
					else:
						file_fail.write(str(r.status_code) + ": " + username + "\n")

					num += 1
					if num == 5:
						num = 0
						time.sleep(10) # reddit api rules limit requests to 30 per minute

			# flush files after every 38 tests
			file_available.flush()
			file_taken.flush()
			file_fail.flush()

file_available.close()
file_taken.close()
file_fail.close()
