#!/usr/bin/python

import Image
import ImageDraw
import sys
import convert


opt_new       = ("new", "n")
opt_taken     = ("taken", "t")
opt_available = ("available", "a")
opt_failed    = ("failed", "fail", "f")
opt_old       = ("old", "o")

color_background    = "#f0f"
color_taken         = "#000"
color_availalve     = "#fff"
color_failed        = "#f00"
color_old_taken     = "#444"
color_old_available = "#bbb"
color_old_failed    = "#b00"


def main():
	if len(sys.argv) < 3:
		help()
		return

	if sys.argv[1] in opt_new:
		new_image(sys.argv[2], color_background)
		return

	img_name = sys.argv[2]
	fname = sys.argv[3]
	color = ""
	fail = False

	if sys.argv[1] in opt_taken:
		color = color_taken
	elif sys.argv[1] in opt_available:
		color = color_availalve
	elif sys.argv[1] in opt_failed:
		color = color_failed
		fail = True
	elif sys.argv[1] in opt_old:
		img_name = sys.argv[3]
		fname = sys.argv[4]

		if sys.argv[2] in opt_taken:
			color = color_old_taken
		elif sys.argv[2] in opt_available:
			color = color_old_available
		elif sys.argv[2] in opt_failed:
			color = color_old_failed
			fail = True
		else:
			help()
			return
	else:
		help()
		return

	plot_data(img_name, fname, color, fail)


def help():
	print "usage: draw.py new <image>"
	print "usage: draw.py [old] <taken|available|failed> <image> <filename>"


def new_image(fname, color):
	size = pow(len(convert.chars),2)
	img = Image.new("RGB", (size,size), color)
	img.save(fname)


def plot_data(img_name, fname, color, fail=False):
	file = open(fname, "r")
	img = Image.open(img_name)
	draw = ImageDraw.Draw(img)

	for line in file:
		name = line.strip()
		if (fail):
			name = name.split(":")[1].strip()
		row = convert.to_num(name[:2])
		col = convert.to_num(name[2:])
		draw.point((col, row), fill=color)

	file.close()
	img.save(img_name)


if __name__ == "__main__":
	main()
