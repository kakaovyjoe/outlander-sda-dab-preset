#!/usr/bin/env python3
"""Read-only inventory/extraction helper for the Outlander SDA NFU package.

The original firmware is never modified. The known archive offset is only a
hint: the script validates the ZIP before trusting it.
"""
from __future__ import annotations

import argparse
import io
import sys
import zipfile
from pathlib import Path

KNOWN_ZIP_OFFSET = 0x1480000
ZIP_SIGNATURE = b"PK\x03\x04"


def open_inner_archive(firmware: Path) -> tuple[zipfile.ZipFile, int, io.BytesIO]:
    size = firmware.stat().st_size
    with firmware.open("rb") as stream:
        candidates = [KNOWN_ZIP_OFFSET]
        # If the known offset changed between firmware versions, look for
        # ZIP local-file signatures. Limit scanning to avoid loading the file.
        chunk_size = 1024 * 1024
        overlap = len(ZIP_SIGNATURE) - 1
        position = 0
        carry = b""
        while position < size:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            data = carry + chunk
            base = position - len(carry)
            start = 0
            while True:
                found = data.find(ZIP_SIGNATURE, start)
                if found < 0:
                    break
                offset = base + found
                if offset not in candidates:
                    candidates.append(offset)
                start = found + 1
            carry = data[-overlap:] if overlap else b""
            position += len(chunk)

    # zipfile needs a seekable view beginning at the embedded archive.
    # Try candidates in ascending order, preferring the previously observed
    # offset. Each candidate is validated by reading the central directory.
    candidates.sort(key=lambda value: (value != KNOWN_ZIP_OFFSET, value))
    for offset in candidates:
        if offset < 0 or offset >= size:
            continue
        with firmware.open("rb") as stream:
            stream.seek(offset)
            payload = stream.read()
        buffer = io.BytesIO(payload)
        try:
            archive = zipfile.ZipFile(buffer)
            archive.infolist()
            return archive, offset, buffer
        except (zipfile.BadZipFile, OSError, EOFError):
            continue
    raise ValueError("V souboru se nepodařilo najít platný vnitřní ZIP archiv.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("firmware", type=Path, help="cesta k původnímu souboru .nfu")
    parser.add_argument(
        "--extract-system",
        type=Path,
        metavar="SLOZKA",
        help="volitelně vyextrahuje pouze bin/system.img do zadané složky",
    )
    args = parser.parse_args()

    if not args.firmware.is_file():
        parser.error(f"Soubor neexistuje: {args.firmware}")

    try:
        archive, offset, _buffer = open_inner_archive(args.firmware)
        with archive:
            print(f"Soubor: {args.firmware}")
            print(f"Velikost: {args.firmware.stat().st_size:,} bajtů")
            print(f"Začátek vnitřního ZIP: 0x{offset:X}")
            print("Obsah archivu:")
            for item in archive.infolist():
                print(f"  {item.file_size:>12,}  {item.filename}")

            if args.extract_system:
                target_name = "bin/system.img"
                try:
                    info = archive.getinfo(target_name)
                except KeyError:
                    raise ValueError(f"Archiv neobsahuje {target_name}.")
                args.extract_system.mkdir(parents=True, exist_ok=True)
                destination = args.extract_system / "system.img"
                with archive.open(info) as source, destination.open("wb") as output:
                    while True:
                        block = source.read(1024 * 1024)
                        if not block:
                            break
                        output.write(block)
                print(f"Vyextrahováno: {destination} ({info.file_size:,} bajtů)")
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"Chyba: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
