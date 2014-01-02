#!/usr/bin/python
import string
import requests
import time
import sys
import smtplib
from base64 import urlsafe_b64encode as url_b64


mode = "sequential"
if sys.argv[1] == "$":
	mode = "file"

start_at = sys.argv[1]
end_at = sys.argv[2]

input_file = sys.argv[2]
output_id  = url_b64(input_file)

fname_available = ""
fname_taken     = ""
fname_fail      = ""

if mode == "sequential":
	fname_available = "names_available_%s-%s.txt" % (start_at, end_at)
	fname_taken     = "names_taken_%s-%s.txt"     % (start_at, end_at)
	fname_fail      = "names_failed_%s-%s.txt"    % (start_at, end_at)
elif mode == "file":
	fname_available = "names_available_%s.txt" % output_id
	fname_taken     = "names_taken_%s.txt"      % output_id
	fname_fail      = "names_failed_%s.txt"    % output_id

file_available = open(fname_available, "w")
file_taken     = open(fname_taken, "w")
file_fail      = open(fname_fail, "w")

chars = string.ascii_lowercase + string.digits + "-_"
agent = "name pinger 1.3 by /u/AnSq"
headers = {"User-Agent": agent}


def main():
	if mode == "sequential":
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
						if username == end_at:
							quit()

						if started:
							ping(username)

							num += 1
							if num == 5:
								num = 0
								time.sleep(10) # reddit api rules limit requests to 30 per minute

					# flush files after every 38 tests
					if started:
						flush()
						print "This batch is processing '%s' to '%s'." % (start_at, end_at)

		quit()

	elif mode == "file":
		num = 0
		input = open(input_file, "r")
		for line in input:
			username = line.strip()
			ping(username)
			num += 1
			if num % 5 == 0:
				time.sleep(10) #ratelimit
			if num % len(chars) == 0:
				flush()
				print "This batch is processing the file '%s' and outputting to '%s'." % (input_file, output_id)
			if num == 5 * len(chars):
				num = 0
		input.close()


def ping(username):
	r = requests.get("http://www.reddit.com/api/username_available.json?user=" + username, headers=headers)
	if r.status_code == 200:
		if r.text == "false":
			print "#  " + username
			file_taken.write(username + "\n")
		elif r.text == "true":
			print "   " + username
			file_available.write(username + "\n")
		else:
			print "-  " + username + " " + str(r.status_code)
			file_fail.write(str(r.status_code) + ": " + username +"\n")
	else:
		print "-  " + username + " " + str(r.status_code)
		file_fail.write(str(r.status_code) + ": " + username + "\n")


def flush():
	file_available.flush()
	file_taken.flush()
	file_fail.flush()


def quit():
	print "Batch finished. Closing files and exiting."
	file_available.close()
	file_taken.close()
	file_fail.close()
	exit()


if __name__ == "__main__":
	main()
