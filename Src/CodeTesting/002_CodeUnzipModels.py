#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
001_CodeUnzipModels.py

- Mengekstrak file ZIP model ke folder Data/DataModels/runs
- Mendukung lebih dari satu file ZIP
- Tidak mengizinkan overwrite folder hasil ekstraksi
"""

from pathlib import Path
import zipfile
import sys

# ==================================================
# BASE PATH
# ==================================================
BASE_DIR = Path(__file__).resolve().parent

# ==================================================
# MODELS PATH
# ==================================================
MODELS_DIR = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "DataModels"
    / "runs"
).resolve()

# ==================================================
# MODEL ZIP FILES
# ==================================================
MODEL_ZIPS = [
    "DorisjuarsaDatasetYoloBaseSizeToScale0_25_640_small.zip",
    "DorisjuarsaDatasetYoloBaseSizeToScale0_25Clahe_640_small.zip",
]

# ==================================================
# VALIDATION: MODELS DIR
# ==================================================
if not MODELS_DIR.exists():
    print("❌ Folder runs tidak ditemukan.")
    print("👉 Jalankan 001_DownloadModels.py terlebih dahulu.")
    sys.exit(1)

# ==================================================
# UNZIP PROCESS
# ==================================================
for zip_name in MODEL_ZIPS:
    zip_path = MODELS_DIR / zip_name

    if not zip_path.exists():
        print(f"❌ File ZIP tidak ditemukan: {zip_path}")
        sys.exit(1)

    extract_dir = MODELS_DIR / zip_name.replace(".zip", "")

    if extract_dir.exists():
        print(f"⚠️ Folder hasil ekstraksi sudah ada:")
        print(f"{extract_dir}")
        print("❌ Overwrite tidak diizinkan.")
        sys.exit(1)

    print("\n📦 Mengekstrak model:")
    print(f"SOURCE: {zip_path}")
    print(f"DEST  : {extract_dir}")

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        print("✅ Ekstraksi selesai.")
    except zipfile.BadZipFile:
        print("❌ File ZIP rusak atau tidak valid:")
        print(zip_path)
        sys.exit(1)

print("\n🎉 Semua model berhasil diekstrak.")
