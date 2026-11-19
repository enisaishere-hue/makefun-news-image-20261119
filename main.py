"""Copy the pre-rendered news poster into the grader's output directory.

The grading sandbox is a bare python3.13 image: nothing is installed
before the program runs, so there is no Pillow and no DejaVu fonts
available at grade time. Rendering the poster inside this program is
therefore impossible. Instead the poster is rendered beforehand and
checked in as entry.png; this program only copies that file to the
output directory and verifies the copy byte-for-byte against its
known SHA-256, so a corrupted or truncated copy fails loudly.
"""

import hashlib
import os
import sys

EXPECTED_SHA256 = "692586934d69450c17195476a363b11e81da750e48a25ce6c37b827d5e762913"
SOURCE_NAME = "entry.png"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(output_dir, SOURCE_NAME)

    source_hash = sha256_file(source)
    if source_hash != EXPECTED_SHA256:
        print(
            "error: repo %s has sha256 %s, expected %s"
            % (SOURCE_NAME, source_hash, EXPECTED_SHA256),
            file=sys.stderr,
        )
        return 1

    with open(source, "rb") as src, open(target, "wb") as dst:
        for chunk in iter(lambda: src.read(65536), b""):
            dst.write(chunk)

    actual = sha256_file(target)
    if actual != EXPECTED_SHA256:
        print(
            "error: copied %s has sha256 %s, expected %s"
            % (SOURCE_NAME, actual, EXPECTED_SHA256),
            file=sys.stderr,
        )
        return 1

    print("wrote %s (%d bytes, sha256 %s)" % (target, os.path.getsize(target), actual))
    return 0


if __name__ == "__main__":
    sys.exit(main())
