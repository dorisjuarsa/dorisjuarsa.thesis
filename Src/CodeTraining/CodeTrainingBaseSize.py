from pathlib import Path
import glob
from datetime import datetime
from ultralytics import YOLO

# ==================================================
# PATH CONFIG (KONSISTEN DENGAN PROJECT)
# ==================================================
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "Datasets"
).resolve()

# DATASET YOLO (HASIL SPLIT)
YOLO_DATASET_DIR = DATA_DIR / "DorisjuarsaDatasetYoloBaseSize"

DATASET_PATH = YOLO_DATASET_DIR / "data.yaml"

if not DATASET_PATH.exists():
    raise FileNotFoundError(f"❌ data.yaml tidak ditemukan:\n{DATASET_PATH}")

# ==================================================
# PILIH MODEL
# ==================================================
# model_name = "yolov8n.pt"
model_name = "yolov8s.pt"
# model_name = "yolov8m.pt"
# model_name = "yolov8l.pt"
# model_name = "yolov8x.pt"

model = YOLO(model_name)

# ==================================================
# NAMA RUN OTOMATIS
# ==================================================
dataset_name = YOLO_DATASET_DIR.name

if "yolov8n" in model_name:
    model_size = "nano"
elif "yolov8s" in model_name:
    model_size = "small"
elif "yolov8m" in model_name:
    model_size = "medium"
elif "yolov8l" in model_name:
    model_size = "large"
elif "yolov8x" in model_name:
    model_size = "xl"
else:
    model_size = "custom"

imgsz = 416
timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
run_name = f"{dataset_name}_{imgsz}_{model_size}_mosaic_scale_{timestamp}"

# ==================================================
# CEK DATASET (SANITY CHECK)
# ==================================================
print("\n--- Pengecekan Dataset ---")


def count_files(dir_path):
    return len(list(dir_path.glob("*.*"))) if dir_path.exists() else 0


print(f"Dataset root: {YOLO_DATASET_DIR}")
print(f"Train images : {count_files(YOLO_DATASET_DIR / 'images' / 'train')}")
print(f"Train labels : {count_files(YOLO_DATASET_DIR / 'labels' / 'train')}")
print(f"Val images   : {count_files(YOLO_DATASET_DIR / 'images' / 'val')}")
print(f"Val labels   : {count_files(YOLO_DATASET_DIR / 'labels' / 'val')}")
print(f"Test images  : {count_files(YOLO_DATASET_DIR / 'images' / 'test')}")
print(f"Test labels  : {count_files(YOLO_DATASET_DIR / 'labels' / 'test')}")
print("--- Pengecekan Dataset Selesai ---\n")

# ==================================================
# TRAINING
# ==================================================
print("🚀 Memulai proses fine-tuning YOLOv8...")

results = model.train(
    data=str(DATASET_PATH),
    epochs=100,
    imgsz=imgsz,
    device=0,
    batch=128,
    name=run_name,
    patience=20,
    cos_lr=True,
    cache=False,
    workers=4,

    # ==================================================
    # AUGMENTASI UTAMA
    # ==================================================
    mosaic=1.0,
    scale=0.3,

    # ==================================================
    # AUGMENTASI RINGAN
    # ==================================================
    fliplr=0.5,
    # hsv_h=0.015,
    # hsv_s=0.7,
    # hsv_v=0.4,

    # ==================================================
    # MATIKAN YANG TIDAK DIPERLUKAN
    # ==================================================
    degrees=0.0,
    translate=0.0,
    shear=0.0,
    perspective=0.0,
    flipud=0.0,
    mixup=0.0,
    copy_paste=0.0,
)

print(f"\n✅ Pelatihan selesai.")
print(f"📁 Hasil tersimpan di: runs/detect/{run_name}")
