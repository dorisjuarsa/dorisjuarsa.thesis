#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
001_CodeDownloadDatasetCvat.py

- Membuat folder dataset dorisjuarsaCvatYolo1.1
- Download file ZIP menggunakan wget ke folder tersebut
- Tidak mengizinkan overwrite jika folder dataset sudah ada
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

zip_path = DATASET_DIR / "dorisjuarsaCvatYolo1.1.zip"

# ==================================================
# SAFETY CHECK: DATASET DIR
# ==================================================
if DATASET_DIR.exists():
    print("⚠️ Folder dataset sudah ada:")
    print(DATASET_DIR)
    print("❌ Untuk menjaga konsistensi data, overwrite tidak diizinkan.")
    print("👉 Hapus atau rename folder tersebut jika ingin download ulang.")
    sys.exit(1)

# ==================================================
# CREATE DIRECTORY
# ==================================================
DATASET_DIR.mkdir(parents=True, exist_ok=False)
print(f"📁 Folder dataset dibuat: {DATASET_DIR}")

# ==================================================
# DOWNLOAD ZIP (WGET)
# ==================================================
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
except subprocess.CalledProcessError:
    print("❌ Gagal mengunduh dataset.")
    sys.exit(1)
