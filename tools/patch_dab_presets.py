#!/usr/bin/env python3
"""Patch only DAB steering-wheel short presses to step through saved presets."""
from __future__ import annotations
import argparse
from pathlib import Path

TARGET = Path("com/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary.smali")
HELPER = r'''
.method private changePresetFromHardKey(I)Z
    .registers 13
    .param p1, "nDirection"    # I (+1 next, -1 previous)
    .prologue
    const v10, 0x101e1
    invoke-virtual {p0, v10}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->getSubjectValue(I)Ljava/lang/Object;
    move-result-object v10
    check-cast v10, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/EntDabModelDefine$eBandMode;
    const v0, 0x101ee
    invoke-virtual {p0, v0}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->getSubjectValue(I)Ljava/lang/Object;
    move-result-object v0
    check-cast v0, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Subject/EntDabPresetList;
    if-eqz v0, :preset_not_found
    invoke-virtual {v0}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Subject/EntDabPresetList;->getTotalSize()I
    move-result v1
    if-lez v1, :preset_not_found

    const v2, 0x101d9
    invoke-virtual {p0, v2}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->getSubjectValue(I)Ljava/lang/Object;
    move-result-object v2
    const/4 v3, 0x0
    if-eqz v2, :current_ready
    check-cast v2, Ljava/lang/Byte;
    invoke-virtual {v2}, Ljava/lang/Byte;->byteValue()B
    move-result v3

    :current_ready
    const/16 v4, 0x12
    if-lez v3, :no_current_preset
    if-gt v3, v4, :no_current_preset
    const/16 v5, 0x11
    goto :scan_init

    :no_current_preset
    const/4 v3, 0x0
    const/16 v5, 0x12
    if-lez p1, :no_current_previous
    goto :scan_init

    :no_current_previous
    const/4 v3, 0x1

    :scan_init
    const/4 v4, 0x0

    :scan_next_slot
    if-ge v4, v5, :preset_not_found
    if-lez p1, :scan_previous
    const/16 v6, 0x12
    if-ne v3, v6, :scan_forward_increment
    const/4 v3, 0x1
    goto :scan_candidate_ready

    :scan_forward_increment
    add-int/lit8 v3, v3, 0x1
    goto :scan_candidate_ready

    :scan_previous
    const/4 v6, 0x1
    if-ne v3, v6, :scan_backward_decrement
    const/16 v3, 0x12
    goto :scan_candidate_ready

    :scan_backward_decrement
    add-int/lit8 v3, v3, -0x1

    :scan_candidate_ready
    add-int/lit8 v6, v3, -0x1
    if-lt v6, v1, :scan_read_item
    goto :scan_skip_slot

    :scan_read_item
    invoke-virtual {v0, v6}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Subject/EntDabPresetList;->getPresetItem(I)Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Subject/EntDabPresetListItem;
    move-result-object v7
    if-eqz v7, :scan_skip_slot

    invoke-virtual {v7}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Subject/EntDabPresetListItem;->getShortservicelabel()Ljava/lang/String;
    move-result-object v8
    if-eqz v8, :scan_check_channel
    invoke-virtual {v8}, Ljava/lang/String;->length()I
    move-result v9
    if-lez v9, :scan_check_channel
    goto :scan_select_preset

    :scan_check_channel
    invoke-virtual {v7}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Subject/EntDabPresetListItem;->getChannel()Ljava/lang/String;
    move-result-object v8
    if-eqz v8, :scan_skip_slot
    invoke-virtual {v8}, Ljava/lang/String;->length()I
    move-result v9
    if-lez v9, :scan_skip_slot

    invoke-virtual {v7}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Subject/EntDabPresetListItem;->getBand()Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/EntDabModelDefine$eBandMode;
    move-result-object v9
    sget-object v8, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/EntDabModelDefine$eBandMode;->ALL:Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/EntDabModelDefine$eBandMode;
    if-ne v10, v8, :check_preset_band
    goto :scan_select_preset

    :check_preset_band
    if-eqz v10, :scan_select_preset
    if-ne v10, v9, :scan_skip_slot

    :scan_select_preset
    new-instance v7, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Command/EntDabModelIndChangePresetCommand;
    int-to-byte v8, v3
    invoke-direct {v7, v8}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Command/EntDabModelIndChangePresetCommand;-><init>(B)V
    invoke-virtual {p0, v7}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->runModel(Lcom/jvckenwood/navi/guiframework/App/Service/CommandCore;)Z
    move-result v0
    return v0

    :scan_skip_slot
    add-int/lit8 v4, v4, 0x1
    goto :scan_next_slot

    :preset_not_found
    const/4 v0, 0x0
    return v0
.end method
'''

def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"Expected one {label} block; found {n}")
    return text.replace(old, new, 1)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("smali_root", type=Path, help="Baksmali output root, containing classes/")
    root = parser.parse_args().smali_root
    path = root / TARGET
    text = path.read_text(encoding="utf-8")
    if ".method private changePresetFromHardKey(I)Z" in text:
        raise RuntimeError("Already patched; refusing to apply twice")

    old_back = """    .line 134
    :pswitch_14
    const/4 v0, 0x1

    .line 136
    iget-object v1, p0, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->mSeekDownCmd:Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Command/EntDabModelIndManualSearchCommand;

    invoke-virtual {p0, v1}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->runModel(Lcom/jvckenwood/navi/guiframework/App/Service/CommandCore;)Z

    goto :goto_e
"""
    new_back = """    .line 134
    :pswitch_14
    const/4 v0, 0x1
    const/4 v1, -0x1
    invoke-direct {p0, v1}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->changePresetFromHardKey(I)Z
    goto :goto_e
"""
    old_forward = """    .line 74
    :pswitch_14
    const/4 v0, 0x1

    .line 76
    iget-object v1, p0, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->mSeekUpCmd:Lcom/jvckenwood/ce/add/guiapp/Entertainment/Model/Dab/Command/EntDabModelIndManualSearchCommand;

    invoke-virtual {p0, v1}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->runModel(Lcom/jvckenwood/navi/guiframework/App/Service/CommandCore;)Z

    goto :goto_e
"""
    new_forward = """    .line 74
    :pswitch_14
    const/4 v0, 0x1
    const/4 v1, 0x1
    invoke-direct {p0, v1}, Lcom/jvckenwood/ce/add/guiapp/Entertainment/Library/EntDabLibrary;->changePresetFromHardKey(I)Z
    goto :goto_e
"""
    text = replace_once(text, old_back, new_back, "backward short press")
    text = replace_once(text, old_forward, new_forward, "forward short press")
    path.write_text(text + "\n" + HELPER, encoding="utf-8")
    print(f"Patched {path}")

if __name__ == "__main__":
    main()
