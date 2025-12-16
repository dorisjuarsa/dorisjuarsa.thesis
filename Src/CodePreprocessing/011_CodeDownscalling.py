#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Downscale object inside YOLO dataset (canvas tetap 360x360)
Author: Doris Juarsa (Final Thesis)
"""

import os
from pathlib import Path
from PIL import Image

# =========================================================
# PATH CONFIG (KONSISTEN DENGAN PROJECT)
# =========================================================
BASE_DIR = Path(__file__).resolve().parent

DATASETS_DIR = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
).resolve()

ORIGINAL_DATASET_ROOT = DATASETS_DIR / "DorisjuarsaDatasetYoloBaseSize"

# =========================================================
# PARAMETER DOWNSCALING
# =========================================================
SCALE_FACTOR = 0.25          # 25% (cell jadi kecil)
IMG_SIZE = (360, 360)

NEW_DATASET_ROOT = DATASETS_DIR / (
    f"DorisjuarsaDatasetYoloBaseSizeToScale{str(SCALE_FACTOR).replace('.', '_')}"
)

print(f"📁 Dataset baru: {NEW_DATASET_ROOT}")

# =========================================================
# CREATE FOLDER STRUCTURE
# =========================================================
for split in ["train", "val", "test"]:
    (NEW_DATASET_ROOT / "images" / split).mkdir(parents=True, exist_ok=True)
    (NEW_DATASET_ROOT / "labels" / split).mkdir(parents=True, exist_ok=True)

# =========================================================
# PROCESS FUNCTION
# =========================================================


def process_image_label(img_path, label_path, out_img_path, out_label_path):
    W, H = IMG_SIZE

    # ---------- IMAGE ----------
    with Image.open(img_path) as img:
        if img.size != IMG_SIZE:
            img = img.resize(IMG_SIZE, Image.LANCZOS)

        new_w = int(W * SCALE_FACTOR)
        new_h = int(H * SCALE_FACTOR)

        img_small = img.resize((new_w, new_h), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), (255, 255, 255))

        px = (W - new_w) // 2
        py = (H - new_h) // 2
        canvas.paste(img_small, (px, py))
        canvas.save(out_img_path)

    # ---------- LABEL ----------
    if not label_path.exists():
        return

    new_lines = []
    with open(label_path) as f:
        for line in f:
            cls, cx, cy, bw, bh = map(float, line.split())

            # absolute
            cx *= W
            cy *= H
            bw *= W
            bh *= H

            # scale from center
            cx_new = W / 2 + (cx - W / 2) * SCALE_FACTOR
            cy_new = H / 2 + (cy - H / 2) * SCALE_FACTOR
            bw_new = bw * SCALE_FACTOR
            bh_new = bh * SCALE_FACTOR

            # normalize
            new_lines.append(
                f"{int(cls)} "
                f"{cx_new / W:.6f} "
                f"{cy_new / H:.6f} "
                f"{bw_new / W:.6f} "
                f"{bh_new / H:.6f}\n"
            )

    with open(out_label_path, "w") as f:
        f.writelines(new_lines)


# =========================================================
# MAIN LOOP
# =========================================================
total = 0
for split in ["train", "val", "test"]:
    src_img_dir = ORIGINAL_DATASET_ROOT / "images" / split
    src_lbl_dir = ORIGINAL_DATASET_ROOT / "labels" / split

    dst_img_dir = NEW_DATASET_ROOT / "images" / split
    dst_lbl_dir = NEW_DATASET_ROOT / "labels" / split

    for img_path in src_img_dir.glob("*.*"):
        name = img_path.stem
        label_path = src_lbl_dir / f"{name}.txt"

        out_img = dst_img_dir / img_path.name
        out_lbl = dst_lbl_dir / f"{name}.txt"

        process_image_label(img_path, label_path, out_img, out_lbl)
        total += 1

print(f"✅ Selesai memproses {total} file")

# =========================================================
# CREATE data.yaml
# =========================================================
yaml_path = NEW_DATASET_ROOT / "data.yaml"
yaml_content = f"""path: {NEW_DATASET_ROOT}
train: images/train
val: images/val
test: images/test

names:
  0: BAS
  1: EOS
  2: NEU
  3: LIM
  4: MON
"""

yaml_path.write_text(yaml_content)
print(f"📝 data.yaml dibuat: {yaml_path}")
