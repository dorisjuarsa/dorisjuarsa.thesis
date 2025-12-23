#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
001_DownloadModels.py

- Membuat folder Data/DataModels/runs
- Download beberapa file model ZIP menggunakan wget
- Tidak mengizinkan overwrite folder runs jika sudah ada
"""

from pathlib import Path
import subprocess
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
# MODEL ZIP URLS
# ==================================================
MODEL_ZIPS = [
    "https://serverdorisjuarsafoldershare.dorisjuarsa.com/DorisjuarsaDatasetYoloBaseSizeToScale0_25_640_small.zip",
    "https://serverdorisjuarsafoldershare.dorisjuarsa.com/DorisjuarsaDatasetYoloBaseSizeToScale0_25Clahe_640_small.zip",
]

# ==================================================
# CHECK FOLDER EXISTENCE
# ==================================================
if MODELS_DIR.exists():
    print(f"⚠️ Folder runs sudah ada:")
    print(f"{MODELS_DIR}")
    print("❌ Untuk menjaga konsistensi eksperimen, overwrite tidak diizinkan.")
    print("👉 Hapus atau rename folder tersebut jika ingin download ulang.")
    sys.exit(1)

# ==================================================
# CREATE DIRECTORY
# ==================================================
MODELS_DIR.mkdir(parents=True, exist_ok=False)
print(f"📁 Folder models dibuat: {MODELS_DIR}")

# ==================================================
# DOWNLOAD ZIP FILES
# ==================================================
for url in MODEL_ZIPS:
    zip_name = Path(url).name
    zip_path = MODELS_DIR / zip_name

    print("\n⬇️  Mengunduh model:")
    print(f"URL : {url}")
    print(f"DEST: {zip_path}")

    try:
        subprocess.run(
            [
                "wget",
                url,
                "-O",
                str(zip_path)
            ],
            check=True
        )
        print("✅ Download selesai.")
    except subprocess.CalledProcessError:
        print("❌ Gagal mengunduh model:")
        print(url)
        sys.exit(1)

print("\n🎉 Semua model berhasil diunduh.")
