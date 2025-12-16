from pathlib import Path
import shutil
import cv2

# ==================================================
# BASE DIR (WAJIB)
# ==================================================
BASE_DIR = Path(__file__).resolve().parent

# ==================================================
# DATASET PATH (KONSISTEN DENGAN PROJECT)
# ==================================================
BASE_DATASET = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
    / "DorisjuarsaDatasetYoloBaseSize"
).resolve()

CLAHE_DATASET = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
    / "DorisjuarsaDatasetYoloBaseSizeClahe"
).resolve()

# ==================================================
# VALIDATION PATH
# ==================================================
if not BASE_DATASET.exists():
    raise FileNotFoundError(
        f"❌ BASE_DATASET tidak ditemukan:\n{BASE_DATASET}"
    )

if not (BASE_DATASET / "labels").exists():
    raise FileNotFoundError(
        f"❌ Folder labels tidak ditemukan:\n{BASE_DATASET / 'labels'}"
    )

# ==================================================
# CLAHE CONFIG
# ==================================================
clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

# ==================================================
# COPY LABELS + YAML
# ==================================================
print("📁 Copy labels & data.yaml...")

if CLAHE_DATASET.exists():
    raise FileExistsError(
        f"❌ Folder target sudah ada:\n{CLAHE_DATASET}"
    )

shutil.copytree(
    BASE_DATASET / "labels",
    CLAHE_DATASET / "labels"
)

shutil.copy2(
    BASE_DATASET / "data.yaml",
    CLAHE_DATASET / "data.yaml"
)

# ==================================================
# APPLY CLAHE TO IMAGES
# ==================================================
print("🖼️ Apply CLAHE ke images...")

for split in ["train", "val", "test"]:
    src_img_dir = BASE_DATASET / "images" / split
    dst_img_dir = CLAHE_DATASET / "images" / split
    dst_img_dir.mkdir(parents=True, exist_ok=True)

    if not src_img_dir.exists():
        raise FileNotFoundError(
            f"❌ Folder images/{split} tidak ditemukan:\n{src_img_dir}"
        )

    for img_path in src_img_dir.glob("*.jpg"):
        img = cv2.imread(str(img_path))
        if img is None:
            raise RuntimeError(f"❌ Gagal baca image: {img_path}")

        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = clahe.apply(l)
        img_clahe = cv2.cvtColor(
            cv2.merge((l, a, b)),
            cv2.COLOR_LAB2BGR
        )

        cv2.imwrite(
            str(dst_img_dir / img_path.name),
            img_clahe
        )

print("\n✅ DATASET CLAHE BERHASIL DIBUAT")
print(f"📂 Base  : {BASE_DATASET}")
print(f"📂 CLAHE: {CLAHE_DATASET}")
