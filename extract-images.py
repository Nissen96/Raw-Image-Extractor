import argparse
import numpy as np
import os
import sys
import typing

from pathlib import Path
from PIL import Image
from tqdm import trange


COMMON_WIDTHS = (800, 1024, 1152, 1280, 1366, 1440, 1600, 1920, 2048)
MODES = ("RGB", "RGBA")


def extract_images(fd: typing.BinaryIO, total_size: int, width: int, height: int, mode: str, offset: int, outdir: Path) -> None:
    channels = len(mode)
    if height is None:
        height = total_size // (width * channels)

    size = width * height * channels
    nimages = total_size // size

    print(f"Extracting {nimages} {mode}-image{'s' if nimages > 1 else ''} ({width}x{height})...")
    fd.seek(offset)
    for i in trange(total_size // size):
        data = np.uint8(list(fd.read(size)))
        img = Image.fromarray(data.reshape((height, width, len(mode))))
        if all(minval == maxval for minval, maxval in img.getextrema()):
            continue

        path = outdir
        filename = "img"
        if nimages > 1:
            path = path / f"{width}x{height}" / mode
            filename += f"-{i * size}.png"
        else:
            filename += f"-{width}x{height}-{mode}.png"

        path.mkdir(parents=True, exist_ok=True)
        img.save(path / filename)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract image from raw data")
    parser.add_argument("infile", type=argparse.FileType("rb"), default=sys.stdin, help="Raw data input file")
    parser.add_argument("--width", type=int, help="Image width")
    parser.add_argument("--height", type=int, help="Image height")
    parser.add_argument("--mode", type=str, choices=MODES, help="Image mode")
    parser.add_argument("--out", default="output", help="Output directory (default: output/)")
    parser.add_argument("--offset", type=int, default=0, help="Data offset")

    args = parser.parse_args()
    args.widths = (args.width,) if args.width is not None else COMMON_WIDTHS
    args.modes = (args.mode,) if args.mode is not None else MODES
    args.out = Path(args.out)

    args.infile.seek(0, os.SEEK_END)
    args.length = args.infile.tell() - args.offset
    return args


def main() -> None:
    args = parse_args()

    for width in args.widths:
        for mode in args.modes:
            extract_images(args.infile, args.length, width, args.height, mode, args.offset, args.out)
            print()


if __name__ == "__main__":
    main()
