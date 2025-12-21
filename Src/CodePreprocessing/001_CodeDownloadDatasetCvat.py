#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
001_CodeDownloadDatasetCvat.py

- Membuat folder dataset dorisjuarsaCvatYolo1.1
- Download file ZIP menggunakan wget ke folder tersebut
"""

from pathlib import Path
import subprocess
import sys

# ==================================================
# BASE PATH
# ==================================================
BASE_DIR = Path(__file__).resolve().parent

# ==================================================
# DATASET PATH
# ==================================================
DATASET_DIR = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
    / "dorisjuarsaCvatYolo1.1"
).resolve()

ZIP_URL = "https://serverdorisjuarsafoldershare.dorisjuarsa.com/dorisjuarsaCvatYolo1.1.zip"

zip_path = (
    DATASET_DIR
    / "dorisjuarsaCvatYolo1.1.zip"
).resolve()

# ==================================================
# CREATE DIRECTORY
# ==================================================
DATASET_DIR.mkdir(parents=True, exist_ok=True)
print(f"📁 Folder dataset siap: {DATASET_DIR}")

# ==================================================
# DOWNLOAD ZIP (WGET)
# ==================================================
if zip_path.exists():
    print(f"⚠️ File ZIP sudah ada, lewati download:\n{zip_path}")
    sys.exit(0)

print("⬇️  Mengunduh dataset menggunakan wget...")
print(f"URL : {ZIP_URL}")
print(f"DEST: {zip_path}")

try:
    subprocess.run(
        [
            "wget",
            ZIP_URL,
            "-O",
            str(zip_path)
        ],
        check=True
    )
    print("✅ Download selesai.")
except subprocess.CalledProcessError as e:
    print("❌ Gagal mengunduh dataset.")
    sys.exit(1)
