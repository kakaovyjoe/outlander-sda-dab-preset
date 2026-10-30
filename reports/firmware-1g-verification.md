# Firmware archive verification – 1G

Date: 2026-10-30

Input file: `S_V4_2_0206_0500_1G_Outlander_RE.zip`

## Verified locally

- Outer ZIP size: 226,680,447 bytes
- Outer ZIP SHA-256: `7a00ba1e544e4a982fa97b05f1f5d9507f7078912448bd1f7bdfc603e9293d3d`
- SHA-256 matches the value independently calculated by the user on Windows.
- ZIP integrity test: passed; no compressed-data errors.
- Expected NK package is present:
  `S_V4_2_0206_0500/NK_V4_2_0206_0500_8G/NaviNk_V4_2_0206_0500.nfu`
- NFU size: 224,537,113 bytes
- NFU SHA-256: `4fcf1bc3bf36d9ae7e50c84d226a6a6a67425fb6f6b0e53e3ce149e7bba4f2da`
- Embedded ZIP begins at offset `0x1480000`; its central directory is readable.
- Embedded package contains 8 entries, including `bin/system.img` (364,904,448 bytes), boot images, BIOS files and `datainfo`.
- `datainfo` identifies `system.img` and its package metadata.

## Interpretation and limits

The uploaded archive is internally consistent with the expected 1G / 4.2.0206.0500 package structure and matches the user's local SHA-256. This does **not** independently authenticate the publisher or prove that the package is an official Mitsubishi release; no trusted vendor checksum/signature has yet been matched.

The original archive was not modified. No firmware was flashed. The full firmware and extracted proprietary binaries are intentionally not committed to this repository.

## Next analysis

Inspect a working copy of `bin/system.img`, then trace the DAB+ hard-key event path and preset-selection code. Any proposed modification must remain analysis-only until a safe, verified recovery route is established.
