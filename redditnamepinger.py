#!/usr/bin/python
import string
import requests
import time
import sys
import smtplib
from email.mime.text import MIMEText
from getpass import getpass


start_at = sys.argv[1]
end_at = sys.argv[2]

fname_available = "names_available_" + start_at + "-" + end_at + ".txt"
fname_taken = "names_taken_" + start_at + "-" + end_at + ".txt"
fname_fail = "names_failed_" + start_at + "-" + end_at + ".txt"

file_available = open(fname_available, "w")
file_taken = open(fname_taken, "w")
file_fail = open(fname_fail, "w")

password = getpass()


def main():


	chars = string.ascii_lowercase + string.digits + "-_"
	agent = "name pinger 1.2 by /u/AnSq"
	headers = {"User-Agent": agent}

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

						num += 1
						if num == 5:
							num = 0
							time.sleep(10) # reddit api rules limit requests to 30 per minute

				# flush files after every 38 tests
				file_available.flush()
				file_taken.flush()
				file_fail.flush()

	quit()


def quit():
	file_available.close()
	file_taken.close()
	file_fail.close()

	mail()

	exit()


def mail():
	email = sys.argv[3]
	server = sys.argv[4]
	port = sys.argv[5]

	smtp = smtplib.SMTP(server, port)
	smtp.starttls()
	smtp.login(email, password)

	sendfile(fname_available, smtp, email)
	sendfile(fname_taken, smtp, email)
	sendfile(fname_fail, smtp, email)

	smtp.quit()


def sendfile(fname, smtp, email):
	f = open(fname, "r")
	m = MIMEText(f.read())
	f.close()

	m["Subject"] = fname
	m["From"] = email
	m["To"] = email

	smtp.sendmail(email, email, m.as_string())



if __name__ == "__main__":
	main()
