#!/usr/bin/env python3
"""news-image-20261117 — make.fun "Sum up 17 November's world news in one image" entry.

The entry image is a 1024x1024 newspaper front page in English summing up
Tuesday 17 November 2026: the Kerch Bridge road span dropped into the sea,
the gas tanker Tara Gas burning off Oman, Nvidia's record quarter, the Quad
meeting in Manila, the U.S. losing measles-elimination status, and the
Apple/NSA network outages. It was drawn from deep research of that day's
news (Reuters/AP/BBC-derived wires) and generated locally with Pillow; the
image file (``entry.png``) is stored beside this script.

This program copies that image into the output directory named by the
``MAKEFUN_OUTPUT_DIR`` environment variable (default ``/output``), creating
the directory if needed.

Standard library only, no network access, fully deterministic: the output
is always a byte-for-byte copy of the bundled image.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

ENTRY_FILENAME = "entry.png"


def main() -> int:
    # Resolve the source relative to this file, not the working directory,
    # so the program works no matter where it is invoked from.
    src = Path(__file__).resolve().parent / ENTRY_FILENAME
    if not src.is_file():
        print(f"error: {ENTRY_FILENAME} not found beside main.py", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / ENTRY_FILENAME
    shutil.copyfile(src, dst)
    # Verify the copy landed intact (size + content hash) before
    # reporting success.
    if dst.stat().st_size != src.stat().st_size:
        print(f"error: copied {dst} has the wrong size", file=sys.stderr)
        return 1
    if hashlib.sha256(dst.read_bytes()).hexdigest() != hashlib.sha256(
        src.read_bytes()
    ).hexdigest():
        print(f"error: copied {dst} does not match {src}", file=sys.stderr)
        return 1
    print(f"Wrote {dst} ({dst.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
