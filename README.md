reddit-name-pinger
==================

reddit-name-pinger is a simple script to determine what 4-character reddit usernames are taken and what's available.

There are 38 valid characters, so there are 38^4 or 2,085,136 valid names. Since reddit limits API requests to 30 per minute, scanning all of them would take just over 48 days if you were doing this on one computer. This is why I have included all of my pre-gathered data in the `data` and `images` folders of this repository. Feel free to play around with it.

The main script can be run with `python redditnamepinger.py [start] [end]`, and it will scan all the names between `[start]` (inclusive) and `[end]` (exclusive). "Between", as used in the previous sentence, is determined by the alphabet in the `chars` variable, which by default has the value `abcdefghijklmnopqrstuvwxyz0123456789-_`.

The script generates three files: `names_available_[start]_[end].txt`, `names_taken_[start]_[end].txt`, and `names_failed_[start]_[end].txt`, each containing a newline-separated list of names that are available for registration, names that are not available, and names that returned some error when trying to access them (a temporary problem). (The failed format is actually slightly different. It includes the HTTP status code that the request to that name returned.)

When you have some data, you can sort (by hand) the three types of files into the folders `data/available`, `data/taken`, and `data/failed`. Then run `python findgaps.py` to merge all of the data into three files in the `data` directory. `findgaps.py` also does some other neat things, including listing all of the data files, reporting some statistics, and, as the name implies, finding gaps in the data. The gaps listed are in the format `[start] [end]`, just like the main script's input parameters.

`findgaps.py` also removes the HTTP status codes from the failed file when it merges it. You can then feed that file to the main script using `python redditnamepinger.py $ [filename] [start]`. The `[start]` parameter is optional, and specifies where in the file the script will start scanning. Unlike in sequential mode, this parameter is exclusive in file mode, meaning that the script will actually begin scanning on the name immediately *after* the one given.

Once the data is collected (even just partially), it can be plotted using `draw.py`. Use `python draw.py new [imagename]` to initialize a new image file with the given name. Use this same name in all subsequent drawing calls. Individual data files can then be added to the image using `python draw.py [available|taken|failed] [imagename] [datafile]`. The first parameter specifies what type of file it is. These can also be shortened to `a`, `t`, and `f`.

The easiest way to draw the entire data set is to sort the files into their respective directories as described above, and then run the following five commands:

	python findgaps.py
	python draw.py n image.png
	python draw.py a image.png data/merged_available.txt
	python draw.py t image.png data/merged_taken.txt
	python draw.py f image.png data/merged_failed.txt

If you only want to plot the data using only a subset of the alphabet (eg. letters only, numbers only, different ordering), change the `chars` variable on line 6 of `convert.py` to the new alphabet.

This image shows some of my results and explains how to interpret the images:

![drawing.png](https://raw2.github.com/AnSq/reddit-name-pinger/master/images/drawing.png)

More images can be found in the `images` folder.
