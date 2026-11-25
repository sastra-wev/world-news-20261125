#!/usr/bin/env python3
"""Deliver the 25 November 2026 front page as /output/entry.png.

"The World in One Page" for Wednesday 25 November 2026 -- led by
Washington's plan to unveil new Section 301 tariffs on 16 trading
partners -- was drawn ahead of time by render.py and is stored in
this repository as entry.png. This program's only job is to hand
those exact bytes to the output directory, unchanged, every run.

Standard library only, no network, no clock, no randomness: two
runs in two fresh sandboxes leave byte-identical files behind. The
asset is checked against the PNG signature, the contest's 1 MiB
cap and its 1024x1024 pixel limit (read from the IHDR header)
before anything is written, and the copy lands under a staging
name first and is moved into place with os.replace, so a reader
never sees a half-written file.
"""

import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DEST = os.path.join(OUT_DIR, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SIZE_CAP = 1048576  # the contest accepts at most 1 MiB
DIM_CAP = 1024      # ... and at most 1024 pixels on either side


def load_asset():
    with open(ASSET, "rb") as fh:
        blob = fh.read()
    if not blob.startswith(PNG_MAGIC):
        raise SystemExit("entry.png lacks the PNG signature")
    if len(blob) > SIZE_CAP:
        raise SystemExit("entry.png is over the 1 MiB cap")
    if len(blob) < 24 or blob[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR header")
    width, height = struct.unpack(">II", blob[16:24])
    if width > DIM_CAP or height > DIM_CAP:
        raise SystemExit("entry.png exceeds 1024x1024 pixels")
    return blob


def deliver(blob):
    os.makedirs(OUT_DIR, exist_ok=True)
    staging = os.path.join(OUT_DIR, ".entry-partial.png")
    with open(staging, "wb") as fh:
        fh.write(blob)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(staging, DEST)


def main():
    blob = load_asset()
    deliver(blob)
    print("wrote {}: {} bytes, sha256 {}".format(
        DEST, len(blob), hashlib.sha256(blob).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
