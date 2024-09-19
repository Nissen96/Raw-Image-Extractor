# Raw Image Extractor

Interpret any binary data as raw pixel values and save as viewable images.

Made for extracting and visualizing the graphical interface of applications stored in process memory dumps - e.g. a Paint windows with a drawing, a Notepad window with unsaved text, or even the entire screen.

The script splits the input data in chunks based on chosen width, height, and mode, and converts each chunk from raw pixel values to a PNG.
The result is a folder of one or more visualizations of the memory/data that can be easily and quickly inspected for graphical artifacts.

A mode option can be set to parse the raw pixel values in a different order, e.g. if stored in `BGR` format instead of `RGB`.

## Installation

Make sure Python is installed, dependencies can be installed with

```
python -m pip install -r requirements.txt
```

## Usage

Only an input file is required. Width, height, and mode can be set if known to reduce the number of output images.
If not set, the script will repeat with several width and mode options, producing a single image per combination.

If the amount of data is large, a height value of 5-10000 is recommended to split the data in multiple smaller images.

Results are stored in the specified output directory, named after the size, mode, and possibly chunk number.

This makes it easy to inspect the memory visually with different assumptions to find any graphical artifacts quickly.

```
usage: extract-images.py [-h] [--width WIDTH] [--height HEIGHT] [--mode MODE] [--out OUT] [--count COUNT] [--offset OFFSET] infile

Extract images from raw data

positional arguments:
  infile           Raw data input file

options:
  -h, --help       Show this help message and exit
  --width WIDTH    Image width
  --height HEIGHT  Image height
  --mode MODE      Image mode within data (e.g. RGB, RGBA, ABGR, BGRx)
  --out OUT        Output directory (default: output/)
  --count COUNT    Number of images (max) extracted per setting
  --offset OFFSET  Offset in bytes (default: 0)
```

If `--width` is not set, the script is repeated for a number of standard screen widths `(800, 1024, 1280, 1366, 1440, 1600, 1920, 2048)`,
extracting images for each option - might take a while but is useful if width is unknown.

If `--mode` is not set, the script will run all extractions assuming both `RGB`, `RGBA`, and `BGRx`.
If set, must contain `R`, `G`, and `B` exactly once, `A` at most once, and `x` any number of times - in any desired order.
`x` is for specifying padding bytes in the storage format used, these are discarded when generating the output image.

If `--height` is not set, a single image is produced for each width and mode combination, visualizing the entire memory at once.
Otherwise, the memory is split into `width x height x channels` chunks and an image extracted for each.
If the amount of data is large, set a height value to avoid a single very large image.

`--count` can be set to specify a maximum number of images to extract per combination of settings, discarding the rest of the data.
If not set, all data will be visualized.

`--offset` can be set to specify a specific data offset in bytes where the extraction should begin.

## Background

A GUI application's window is typically stored as raw image data (array of pixel values with no image format) within its process memory.
This makes it possible to dump a process' memory and extract its graphics to see the contents at the time of the dump.

This is helpful in memory analysis where the contents of e.g. Paint, Notepad, the browser, or the entire screen can be difficult to extract but easy to inspect visually.

The mode flag is useful, since process memory in e.g. Windows stores the graphics in 32-bit `BGRx` format, where `x` is just a padding byte and should be discarded.
Visualizing such data with an RGB, or RGBA assumption results in a useless interpretation.

To extract the memory of a specific process from a memory dump, use Volatility - explanation below for Volatility 3:

1. Find the process ID with one of the plugins `windows.pslist`, `windows.pstree`, or `windows.psscan`.
2. Dump the memory with the plugin `windows.memmap --pid <PID> --dump`.
    - This often dumps a too large portion of memory but starts from the process' own memory. This is where the `--count` option is useful to only extract images from the relevant part of the dump.
3. Use `python3 extract-images.py --height 8000 pid.<PID>.DMP` (possibly with `--count 3` or similar to truncate)
4. Inspect image outputs in `output/`
