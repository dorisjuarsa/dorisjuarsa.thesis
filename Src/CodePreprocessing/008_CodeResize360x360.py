from pathlib import Path
import cv2
import shutil
import sys

# ===== lokasi script =====
BASE_DIR = Path(__file__).resolve().parent

# ===== path dataset =====
DATA_DIR = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
    / "dorisjuarsaCvatYolo1.1"
    / "data"
).resolve()

SRC_DIR = DATA_DIR / "merge"
OUT_DIR = DATA_DIR / "merge_resize_360x360"

TARGET_SIZE = (360, 360)  # (width, height)

# ===== validasi =====
if not SRC_DIR.exists():
    print(f"[ERROR] Folder merge tidak ditemukan: {SRC_DIR}")
    sys.exit(1)

if OUT_DIR.exists():
    print(f"[STOP] Folder merge_resize sudah ada: {OUT_DIR}")
    sys.exit(0)

OUT_DIR.mkdir(parents=True)
print(f"[OK] Folder merge_resize dibuat: {OUT_DIR}")

# ===== proses =====
processed = 0
skipped = 0

for img_path in SRC_DIR.glob("*.jpg"):
    txt_path = SRC_DIR / f"{img_path.stem}.txt"

    # pastikan pasangan YOLO ada
    if not txt_path.exists():
        skipped += 1
        continue

    # baca image
    img = cv2.imread(str(img_path))
    if img is None:
        skipped += 1
        continue

    # resize image
    resized = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_AREA)

    # simpan image resize
    cv2.imwrite(str(OUT_DIR / img_path.name), resized)

    # copy txt TANPA perubahan
    shutil.copy(txt_path, OUT_DIR / txt_path.name)

    processed += 1

# ===== laporan =====
print("\n=== SELESAI ===")
print(f"Image di-resize : {processed}")
print(f"Dilewati        : {skipped}")
print(f"Output          : {OUT_DIR}")
