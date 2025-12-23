#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
002_CodeUnzipDatasetCvat.py

- Mengekstrak dataset CVAT YOLO dari ZIP
- Folder output: dorisjuarsaCvatYolo1.1/data
- Folder data boleh belum ada (akan dibuat)
- Overwrite folder data yang sudah berisi TIDAK diizinkan
"""

from pathlib import Path
import zipfile
import sys

# ==================================================
# BASE PATH
# ==================================================
BASE_DIR = Path(__file__).resolve().parent

# ==================================================
# PATH CONFIG
# ==================================================
DATASET_ROOT = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
    / "dorisjuarsaCvatYolo1.1"
).resolve()

zip_path = DATASET_ROOT / "dorisjuarsaCvatYolo1.1.zip"
extract_to = DATASET_ROOT / "data"

# ==================================================
# VALIDATION: ZIP FILE
# ==================================================
if not zip_path.exists():
    print(f"❌ File ZIP tidak ditemukan:\n{zip_path}")
    sys.exit(1)

if not zipfile.is_zipfile(zip_path):
    print(f"❌ File ditemukan tapi bukan ZIP valid:\n{zip_path}")
    sys.exit(1)

# ==================================================
# SAFETY CHECK: OUTPUT DIR
# ==================================================
if extract_to.exists():
    if any(extract_to.iterdir()):
        print("⚠️ Folder data sudah ada dan tidak kosong:")
        print(extract_to)
        print("❌ Overwrite tidak diizinkan.")
        print("👉 Hapus atau rename folder data jika ingin unzip ulang.")
        sys.exit(1)
else:
    extract_to.mkdir(parents=True, exist_ok=False)
    print(f"📁 Folder output dibuat: {extract_to}")

# ==================================================
# UNZIP PROCESS
# ==================================================
print("\n📦 Mengekstrak dataset:")
print(f"SOURCE: {zip_path}")
print(f"DEST  : {extract_to}")

try:
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print("✅ Unzip selesai.")
except Exception as e:
    print(f"❌ Gagal unzip: {e}")
    sys.exit(1)
