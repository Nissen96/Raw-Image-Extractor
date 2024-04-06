# Raw Image Extractor

Script for extracting raw image data as images from binary files.

Can be used on any binary data, but very useful for memory dumps, specifically process memory dumped with e.g. Volatility.
This makes it easy to e.g. dump the process memory of Paint and see the drawing,
or dump basically any process and get a screenshot of the entire screen.

Not recommended for use on entire memory dumps, the smaller the binary file, the faster the process and the fewer the results.

## Installation

Make sure Python is installed, dependencies can be installed with

```
python -m pip install -r requirements.txt
```

## Usage

Only an input file is required, but image width, height and mode (RGB/RGBA) can be provided if known, reducing the number of outputs:

```
usage: extract-images.py [-h] [--width WIDTH] [--height HEIGHT] [--mode {RGB,RGBA}]
                  [--out OUT] [--offset OFFSET]
                  infile

Extract image from raw data

positional arguments:
  infile             Raw data input file

options:
  -h, --help         Show this help message and exit
  --width WIDTH      Image width
  --height HEIGHT    Image height
  --mode {RGB,RGBA}  Image mode
  --out OUT          Output directory (default: output/)
  --offset OFFSET    Data offset
```

If `--width` is not set, the script is repeated for a number of standard screen resolutions `(800, 1024, 1152, 1280, 1366, 1440, 1600, 1920, 2048)`,
extracting images for each option - might take a while but is useful if width is unknown.

If `--mode` is not set, the script will run all extractions for both RGB- and RGBA-mode.

If `--height` is not set, only a single, tall image is produced (based on the width and mode), visualizing the enitre memory at once.
Otherwise, the memory is split into `width x height x channels` chunks and an image extracted for each.

`--offset` can be set to specify a specific data offset where the extraction should begin.

Results are stored in the specified output directory, possibly split into subfolders based on resolution and channel.
