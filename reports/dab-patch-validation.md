# DAB steering-wheel preset patch – validation report

Date: 2026-10-31

## Confirmed from the original 1G APK

- `EntDabLibrary` receives hard forward/backward skip events. The event enum maps ordinal 2 to `SHORTPRESS`; this is the exact event changed below.
- A short press on either DAB hard-skip event originally sends the DAB manual-search command (up/down).
- The on-screen DAB preset UI uses `EntDabModelIndChangePresetCommand` with one-based preset numbers.
- The DAB model exposes the current preset number through subject `0x101d9`.
- The full preset list is exposed through subject `0x101ee`; the UI displays three banks of six positions, numbered 1–18.
- A slot is occupied when either its short service label or channel text is non-empty.
- The UI also filters populated slots by the selected DAB band in subject `0x101e1`: it allows all bands in `ALL` mode, otherwise only a matching band. The patch mirrors this rule.
- The existing DAB command dispatch sends the explicit preset number to the native DAB layer.

## Patch behavior

Only the DAB hard forward/back **SHORTPRESS** handlers are changed:

- Right/forward short press selects the next occupied eligible preset.
- Left/back short press selects the previous occupied eligible preset.
- It checks all 18 positions, skips empty slots and band-mismatched slots, and wraps at both ends.
- If only one eligible preset exists, a full scan returns to that same preset rather than doing nothing.
- If no current preset is reported, forward starts at preset 1 and backward starts at preset 18.
- Selection is sent through the original `EntDabModelIndChangePresetCommand`.

The on-screen search controls are untouched. Long-press, repeat-press and seek-stop paths are untouched. The patch does not change volume handling or the up/down volume keys.

## Static tests and build validation

GitHub Actions run: [41196044899](https://github.com/kakaovyjoe/outlander-sda-dab-preset/actions/runs/41196044899)

- Reassembly of the two uploaded APK parts and original APK SHA-256 check succeeded.
- DEX disassembly succeeded.
- Patch script completed, and Smali assembly of the modified DEX succeeded.
- Repacked APK ZIP integrity check succeeded.
- A separate algorithm simulation passed checks for next/previous direction, wrap-around, empty-slot skipping, band filtering, and the one-preset case.

Hashes:
- Original APK SHA-256: `7155c4429bee06cc2066c6500b3ae5afa9e7d2187303e1cd62738abbed0c0ad8`
- Patched `classes.dex` SHA-256: `84007435c3e87a02ae2234178ab2568bd500f9a94975c4b84388d88decc00d55`
- Unsigned validation APK SHA-256: `66d4a5fa31f84eb6f7a9fccfb23d544473d1ef0fd60089b83254a9be44efa2b7`

## Important installation limitation

The original APK's v1 certificate subject is `CN=Android Debug, O=Android, C=US` (SHA-256 fingerprint `DD:B1:20:E4:C2:93:A6:0F:8C:A8:6F:0D:47:84:AB:21:93:F3:C2:5A:1A:E6:87:D8:AD:8D:3B:D4:43:EF:6E:78`). The private signing key is not embedded in the APK; only the public certificate/signature data is present. Changing `classes.dex` invalidates the original signature.

Therefore `GuiApp-patched-unsigned.apk` is a **validation artifact only**, not an installation package. Do not install it or copy it into the firmware. Before any in-vehicle test, the correct system-app signing/update path and a verified recovery method must be established. No change has been installed in the vehicle.
