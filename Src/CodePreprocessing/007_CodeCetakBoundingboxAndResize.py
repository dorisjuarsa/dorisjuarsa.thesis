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
OUT_DIR = DATA_DIR / "merge_resize_vis"

TARGET_SIZE = (360, 360)  # (width, height)

# ===== warna per kelas =====
CLASS_COLOR = {
    "BAS": (0, 0, 255),
    "EOS": (0, 255, 0),
    "NEU": (255, 0, 0),
    "LIM": (0, 255, 255),
    "MON": (255, 0, 255),
}

# ===== validasi =====
if not SRC_DIR.exists():
    print(f"[ERROR] Folder merge tidak ditemukan: {SRC_DIR}")
    sys.exit(1)

if OUT_DIR.exists():
    print(f"[STOP] Folder merge_resize_vis sudah ada: {OUT_DIR}")
    sys.exit(0)

OUT_DIR.mkdir(parents=True)
print(f"[OK] Folder merge_resize_vis dibuat: {OUT_DIR}")

processed = 0
skipped = 0

print("\n=== PROSES RESIZE + VISUALISASI ===")

for img_path in SRC_DIR.glob("*.jpg"):
    txt_path = SRC_DIR / f"{img_path.stem}.txt"

    # pastikan pasangan YOLO ada
    if not txt_path.exists():
        skipped += 1
        continue

    img = cv2.imread(str(img_path))
    if img is None:
        skipped += 1
        continue

    # ===== resize image =====
    resized = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_AREA)
    h, w, _ = resized.shape

    # ===== baca label =====
    with txt_path.open("r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        parts = line.split()
        if len(parts) != 5:
            continue

        _, xc, yc, bw, bh = map(float, parts)

        # YOLO → pixel (SETELAH resize)
        x1 = int((xc - bw / 2) * w)
        y1 = int((yc - bh / 2) * h)
        x2 = int((xc + bw / 2) * w)
        y2 = int((yc + bh / 2) * h)

        # ambil kelas dari nama file
        cls = img_path.stem.split("_")[0]
        color = CLASS_COLOR.get(cls, (255, 255, 255))

        # gambar bbox
        cv2.rectangle(resized, (x1, y1), (x2, y2), color, 2)

        # teks label
        cv2.putText(
            resized,
            cls,
            (x1, max(y1 - 8, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # ===== simpan output =====
    cv2.imwrite(str(OUT_DIR / img_path.name), resized)

    # copy txt TANPA perubahan
    shutil.copy(txt_path, OUT_DIR / txt_path.name)

    processed += 1

print("\n=== SELESAI ===")
print(f"Gambar diproses : {processed}")
print(f"Dilewati        : {skipped}")
print(f"Output          : {OUT_DIR}")
