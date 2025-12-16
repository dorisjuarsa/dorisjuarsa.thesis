from pathlib import Path
import shutil
import cv2

# ==================================================
# BASE DIR (KONSISTEN DENGAN PROJECT)
# ==================================================
BASE_DIR = Path(__file__).resolve().parent

# ==================================================
# DATASET PATH
# ==================================================
BASE_DATASET = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
    / "DorisjuarsaDatasetYoloBaseSizeToScale0_25"
).resolve()

CLAHE_DATASET = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
    / "DorisjuarsaDatasetYoloBaseSizeToScale0_25Clahe"
).resolve()

# ==================================================
# VALIDATION
# ==================================================
if not BASE_DATASET.exists():
    raise FileNotFoundError(
        f"❌ BASE_DATASET tidak ditemukan:\n{BASE_DATASET}"
    )

if not (BASE_DATASET / "images").exists():
    raise FileNotFoundError(
        f"❌ Folder images tidak ditemukan:\n{BASE_DATASET / 'images'}"
    )

if not (BASE_DATASET / "labels").exists():
    raise FileNotFoundError(
        f"❌ Folder labels tidak ditemukan:\n{BASE_DATASET / 'labels'}"
    )

if CLAHE_DATASET.exists():
    raise FileExistsError(
        f"❌ Folder target sudah ada (hapus dulu jika mau regenerate):\n{CLAHE_DATASET}"
    )

# ==================================================
# CLAHE CONFIG
# ==================================================
CLAHE_CLIP = 2.0
CLAHE_TILE = (8, 8)

clahe = cv2.createCLAHE(
    clipLimit=CLAHE_CLIP,
    tileGridSize=CLAHE_TILE
)

# ==================================================
# COPY LABELS
# ==================================================
print("📁 Copy labels...")

shutil.copytree(
    BASE_DATASET / "labels",
    CLAHE_DATASET / "labels"
)

# ==================================================
# GENERATE data.yaml (AUTO PATH)
# ==================================================
print("📝 Generate data.yaml (auto path)...")

base_yaml_text = (BASE_DATASET / "data.yaml").read_text()

fixed_yaml_text = base_yaml_text.replace(
    f"path: {BASE_DATASET.as_posix()}",
    f"path: {CLAHE_DATASET.as_posix()}"
)

(CLAHE_DATASET / "data.yaml").write_text(fixed_yaml_text)

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
            raise RuntimeError(
                f"❌ Gagal membaca image:\n{img_path}"
            )

        # --- CLAHE on L channel ---
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l_clahe = clahe.apply(l)
        img_clahe = cv2.cvtColor(
            cv2.merge((l_clahe, a, b)),
            cv2.COLOR_LAB2BGR
        )

        cv2.imwrite(
            str(dst_img_dir / img_path.name),
            img_clahe
        )

print("\n✅ DATASET CLAHE BERHASIL DIBUAT")
print(f"📂 BASE  : {BASE_DATASET}")
print(f"📂 CLAHE: {CLAHE_DATASET}")
print("🚀 Siap untuk training YOLO (komparasi base vs CLAHE)")
