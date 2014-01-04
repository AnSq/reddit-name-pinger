#!/usr/bin/python

import Image
import ImageDraw
import sys
import convert


opt_new       = ("new", "n")
opt_taken     = ("taken", "t")
opt_available = ("available", "a")
opt_failed    = ("failed", "fail", "f")

color_background    = "#f0f"
color_taken         = "#000"
color_availalve     = "#fff"
color_failed        = "#f00"


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

	if sys.argv[1] in opt_taken:
		color = color_taken
	elif sys.argv[1] in opt_available:
		color = color_availalve
	elif sys.argv[1] in opt_failed:
		color = color_failed
	else:
		help()
		return

	plot_data(img_name, fname, color)


def help():
	print "usage: draw.py new|n <image>"
	print "       draw.py <taken|t|available|a|failed|f> <image> <filename>"


def new_image(fname, color):
	size = pow(len(convert.chars),2)
	img = Image.new("RGB", (size,size), color)
	img.save(fname)


def plot_data(img_name, fname, color):
	file = open(fname, "r")
	img = Image.open(img_name)
	draw = ImageDraw.Draw(img)

	for line in file:
		name = line.strip()
		row = convert.to_num(name[:2])
		col = convert.to_num(name[2:])
		draw.point((col, row), fill=color)

	file.close()
	img.save(img_name)


if __name__ == "__main__":
	main()
