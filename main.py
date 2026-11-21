#!/usr/bin/env python3
"""Starlight Arriving — make.fun entry for "Make the AI judge feel awe".

The program writes one fixed text to /output/entry.txt. The text is
meant to slow the reader down: short clauses, soft consonants, and one
image — starlight that left its star before any word the reader has
ever read was written, and only arrives now. Nothing is instructed;
the calm comes from the image itself.

The text is 272 Unicode code points, inside the competition's 1-280
gate. The program is deterministic and makes no network calls.
"""

import os
import sys
import tempfile
from pathlib import Path

# The competition's gate: the entry text must be 1-280 characters.
MAX_CHARS = 280
MIN_CHARS = 1

TEXT = (
    "All day, words have passed through you like weather. "
    "Tonight a star still burns that lit before the first of them was written. "
    "Its light has travelled all this time, in no hurry, and arrives now, soft as dew. "
    "It asks nothing. "
    "It will still be here when this sentence ends."
)

OUTPUT_PATH = "/output/entry.txt"


def entry_text() -> str:
    """Return the entry text, failing loudly if it ever leaves the gate."""
    if not MIN_CHARS <= len(TEXT) <= MAX_CHARS:
        raise SystemExit(
            f"entry text is {len(TEXT)} characters, must be "
            f"{MIN_CHARS}-{MAX_CHARS}"
        )
    if not TEXT.strip():
        raise SystemExit("entry text is only whitespace")
    return TEXT


def main() -> int:
    text = entry_text()
    out = Path(OUTPUT_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    # Write atomically: a reader never sees a half-written entry.
    fd, tmp = tempfile.mkstemp(dir=str(out.parent), prefix=out.name + ".")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, out)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    print(f"wrote {OUTPUT_PATH} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
