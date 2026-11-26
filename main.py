#!/usr/bin/env python3
"""The World in One Page -- Wednesday 25 November 2026.

The front page was rendered ahead of time and is stored beside this
file as entry.png. This program only carries it to the output
directory: it reads the pre-rendered entry.png, checks it with the
standard library alone (PNG signature, size at most 1 MiB, dimensions
at most 1024x1024 taken from the IHDR chunk), and writes the exact
same bytes out.

Run it:  python3 main.py   ->  writes entry.png to
$MAKEFUN_OUTPUT_DIR when that variable is set, to /output/entry.png
otherwise (creating the directory first when its parent allows), and
to entry.png in the current working directory as a last resort.
Every writable destination gets the same bytes, and the run fails
only if no destination at all accepts the file.

Standard library only: nothing is installed before the grader runs
this, so no third-party import may appear here.
"""

import os
import struct
import sys

MAX_BYTES = 1 << 20       # 1 MiB, the entry size limit
MAX_SIDE = 1024           # entries are at most 1024x1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_entry():
    """Return the pre-rendered page bytes, validated with stdlib only."""
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    with open(source, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB limit"
                         % len(data))
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png does not start with the PNG signature")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0 or width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError("entry.png is %dx%d, over the 1024x1024 limit"
                         % (width, height))
    return data


def destinations():
    """Output paths to try, in priority order."""
    targets = []
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError:
            pass
        targets.append(os.path.join(out_dir, "entry.png"))
    try:
        os.makedirs("/output", exist_ok=True)
    except OSError:
        pass
    if os.path.isdir("/output"):
        targets.append("/output/entry.png")
    try:
        cwd = os.getcwd()
    except OSError:
        cwd = None
    if cwd:
        targets.append(os.path.join(cwd, "entry.png"))
    return targets


def main():
    data = read_entry()
    saved = False
    last_error = None
    for path in destinations():
        try:
            with open(path, "wb") as handle:
                handle.write(data)
            saved = True
        except OSError as exc:
            last_error = exc
    if not saved:
        if last_error is not None:
            raise last_error
        sys.exit("no writable output destination for entry.png")


if __name__ == "__main__":
    main()
