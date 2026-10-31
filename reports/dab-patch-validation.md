# DAB steering-wheel preset patch – validation report

Date: 2026-10-31

## Confirmed from the original 1G APK

- The DAB library handles the hard forward/backward skip events separately from the on-screen forward/back skip controls.
- A short press on either hard-skip event originally sends the DAB manual-search command (up/down).
- The DAB model exposes the current one-based preset number through subject `0x101d9`.
- The complete preset list is exposed through subject `0x101ee`.
- Preset numbers are one-based: bank 1 = 1–6, bank 2 = 7–12, bank 3 = 13–18.
- The existing preset UI checks a slot by its short service label or channel text; the patch applies the same occupied-slot rule.
- The existing DAB model command `EntDabModelIndChangePresetCommand` sends an explicit preset number to the native DAB layer.

## Patch behavior

The patch script changes only the DAB hard forward/back short-press handlers:

- right/forward short press: next occupied preset;
- left/back short press: previous occupied preset;
- scans all 18 positions and wraps at both ends;
- empty positions are skipped;
- uses the existing change-preset model command.

The on-screen DAB search controls are unchanged. Long-press/repeat-search paths are unchanged. Volume controls are not handled by `EntDabLibrary` and are not modified by this patch.

## Build validation

GitHub Actions run: [41194937933](https://github.com/kakaovyjoe/outlander-sda-dab-preset/actions/runs/41194937933)

- Original APK SHA-256: `7155c4429bee06cc2066c6500b3ae5afa9e7d2187303e1cd62738abbed0c0ad8`
- Patched classes.dex SHA-256: `337a89b23f699ff56cb9ae4da13e2251b5e4f6ed776b99cc44f6caf752d387be`
- Unsigned preview APK SHA-256: `79454feaacd8b394dd562700d9b459bf7b883a64d715be4d8f381297bfe54225`
- Smali assembly succeeded.
- Repacked APK ZIP integrity check succeeded.

## Important installation limitation

The original APK contains a v1 signing certificate whose subject is `CN=Android Debug, O=Android, C=US`. The APK contains only the public certificate/signature data, not the original private signing key. Changing `classes.dex` invalidates the original APK signature.

Therefore `GuiApp-patched-unsigned.apk` is a validation artifact only. It is **not installable and must not be copied into the firmware or flashed**. Before any in-vehicle test, the signing/update mechanism and a verified recovery route must be established. No change has been installed in the vehicle.
