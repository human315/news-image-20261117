#!/usr/bin/env python3
"""news-image-20261117 entry: copy the bundled entry.png to the output directory.

Output directory: $MAKEFUN_OUTPUT_DIR, or /output by default (per starter/main.ts).
The copy is byte-for-byte, so repeated runs produce identical output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )

if __name__ == "__main__":
    main()
    sys.exit(0)
