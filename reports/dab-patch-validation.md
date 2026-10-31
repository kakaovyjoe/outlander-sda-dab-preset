# DAB steering-wheel preset patch – validation report

Date: 2026-10-31

## Confirmed from the original 1G APK

- `EntDabLibrary` receives separate hard forward/backward skip events. The event enum maps ordinal 2 to `SHORTPRESS`; this is the exact event changed by the patch.
- Originally, a DAB hard-skip short press sends the manual-search command (up/down).
- The on-screen DAB preset UI uses `EntDabModelIndChangePresetCommand` with one-based preset numbers.
- Current preset number is provided by subject `0x101d9` (a `Byte`).
- The full preset list is provided by subject `0x101ee`; the UI uses three banks of six positions, numbered 1–18.
- A preset slot is occupied when either its short service label or channel text is non-empty.
- The selected band is provided by subject `0x101e1`. The UI permits all populated slots in `ALL` mode; otherwise, it permits only a slot whose band matches the selected band. A missing selected-band value is not treated as `ALL`.
- The existing DAB command dispatch sends the explicit one-based preset number to the native DAB layer.

## Patch behavior

Only the DAB hard forward/back **SHORTPRESS** handlers are changed:

- Right/forward short press selects the next occupied eligible preset.
- Left/back short press selects the previous occupied eligible preset.
- It scans the full 18-position list, skips empty and band-mismatched slots, and wraps at both ends.
- If only one eligible preset exists, a full cycle returns to that preset.
- If the current preset is not reported, forward begins before slot 1 and backward begins before slot 18.
- Selection is sent through the original `EntDabModelIndChangePresetCommand`.

The on-screen search controls are untouched. Long-press, repeat-press, and seek-stop paths are untouched. The patch does not change volume handling or the up/down volume keys.

## Static build validation

GitHub Actions run: [41196543678](https://github.com/kakaovyjoe/outlander-sda-dab-preset/actions/runs/41196543678)

- Reassembly of the uploaded APK parts and original APK SHA-256 check succeeded.
- DEX disassembly succeeded.
- The patch script completed and the modified Smali assembled back into DEX.
- The repacked APK ZIP integrity check succeeded.
- A separate algorithm model passed nine cases: next/previous direction, wrap at both ends, empty-slot skipping, band filtering, no-current-preset start position, and the single-preset case.

Hashes:
- Original APK SHA-256: `7155c4429bee06cc2066c6500b3ae5afa9e7d2187303e1cd62738abbed0c0ad8`
- Patched `classes.dex` SHA-256: `c96d40bf3104ac5e25738204bfc78efd9d36532fbc629d96d05f03a4cd478189`
- Unsigned validation APK SHA-256: `8d319bc7f29f5000289b7613fd91e51c081199c0ca89790abaafbcf3887c6ddc`

## Installation limitation

The original APK has a v1 certificate with subject `CN=Android Debug, O=Android, C=US`. Its private signing key is not embedded in the APK; only the public certificate and signature data are present. Changing `classes.dex` invalidates the original signature.

Therefore, `GuiApp-patched-unsigned.apk` is only a validation artifact, not an installable package. Do not install it or put it into the vehicle firmware. No system image has been changed, no firmware package has been rebuilt, and no change has been installed in the vehicle.

A successful static build does not establish that the radio will accept a modified system image or that the unit can be recovered if an update fails. The only safe next step is to confirm the authorised service/update path and a proven recovery procedure before considering any in-vehicle test.
