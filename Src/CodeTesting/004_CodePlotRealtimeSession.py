#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot Realtime Session CSV (Qt / PySide6)
Input : session.csv from Data/DataTesting/Output/Realtime/<session_folder>/
Output: plots/*.png + summary.txt inside the same session folder.

Usage:
  python Src/CodeReport/CodePlotRealtimeSessionQt.py
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox


def project_root_from_this_file() -> Path:
    # This file: Src/CodeReport/CodePlotRealtimeSessionQt.py
    # parents[0]=CodeReport, [1]=Src, [2]=project_root
    return Path(__file__).resolve().parents[2]


def pick_csv_file_qt(default_root: Path) -> Path | None:
    app = QApplication.instance() or QApplication(sys.argv)

    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Pilih session.csv",
        str(default_root),
        "CSV files (*.csv)"
    )
    return Path(file_path).resolve() if file_path else None


def ensure_plots_dir(csv_path: Path) -> Path:
    session_dir = csv_path.parent
    plots_dir = session_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    return plots_dir


def parse_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    # Expected: YYYY-MM-DD HH:MM:SS.mmm
    if "timestamp" in df.columns:
        df["timestamp_dt"] = pd.to_datetime(df["timestamp"], errors="coerce")
    else:
        df["timestamp_dt"] = pd.NaT
    return df


def rolling_mean(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=max(2, window // 3)).mean()


def savefig(path: Path):
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def main():
    # Setup Qt app
    app = QApplication.instance() or QApplication(sys.argv)

    project_root = project_root_from_this_file()
    default_root = (project_root / "Data" / "DataTesting" /
                    "Output" / "Realtime").resolve()
    default_root.mkdir(parents=True, exist_ok=True)

    csv_path = pick_csv_file_qt(default_root)
    if not csv_path:
        return  # user cancelled

    if not csv_path.exists():
        QMessageBox.critical(
            None, "Error", f"File tidak ditemukan:\n{csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Gagal membaca CSV:\n{e}")
        return

    if df.empty:
        QMessageBox.critical(None, "Error", "CSV kosong.")
        return

    df = parse_timestamp(df)

    required = ["frame_idx", "inference_ms",
                "fps_inst", "clahe_on", "total_objects"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        QMessageBox.critical(None, "Error", f"Kolom wajib hilang:\n{missing}")
        return

    # detect count_* columns dynamically
    count_cols = [c for c in df.columns if c.startswith("count_")]

    # sort by frame idx
    df = df.sort_values("frame_idx").reset_index(drop=True)
    x = df["frame_idx"].astype(int).to_numpy()

    plots_dir = ensure_plots_dir(csv_path)

    # Rolling windows (approx 1s / 3s based on median fps)
    fps_med = float(np.nanmedian(
        df["fps_inst"].replace([np.inf, -np.inf], np.nan)))
    if not np.isfinite(fps_med) or fps_med <= 0:
        fps_med = 10.0
    win_1s = int(max(5, round(fps_med)))
    win_3s = int(max(10, round(fps_med * 3)))

    # 01 - inference time
    plt.figure()
    plt.plot(x, df["inference_ms"].to_numpy(), label="inference_ms")
    plt.plot(x, rolling_mean(df["inference_ms"], win_1s).to_numpy(
    ), label=f"rolling ~1s (win={win_1s})")
    plt.plot(x, rolling_mean(df["inference_ms"], win_3s).to_numpy(
    ), label=f"rolling ~3s (win={win_3s})")
    plt.xlabel("frame_idx")
    plt.ylabel("inference_ms")
    plt.title("Realtime Inference Time per Frame")
    plt.legend()
    savefig(plots_dir / "01_inference_ms.png")

    # 02 - fps
    fps_series = df["fps_inst"].replace([np.inf, -np.inf], np.nan)
    plt.figure()
    plt.plot(x, fps_series.to_numpy(), label="fps_inst")
    plt.plot(x, rolling_mean(fps_series, win_1s).to_numpy(),
             label=f"rolling ~1s (win={win_1s})")
    plt.plot(x, rolling_mean(fps_series, win_3s).to_numpy(),
             label=f"rolling ~3s (win={win_3s})")
    plt.xlabel("frame_idx")
    plt.ylabel("fps")
    plt.title("Realtime FPS (Instant & Smoothed)")
    plt.legend()
    savefig(plots_dir / "02_fps_inst.png")

    # 03 - total objects per frame
    plt.figure()
    plt.plot(x, df["total_objects"].to_numpy(), label="total_objects")
    plt.plot(x, rolling_mean(df["total_objects"], win_1s).to_numpy(
    ), label=f"rolling ~1s (win={win_1s})")
    plt.xlabel("frame_idx")
    plt.ylabel("objects")
    plt.title("Total Detections per Frame")
    plt.legend()
    savefig(plots_dir / "03_total_objects.png")

    # 04 - stacked per class (if available)
    if count_cols:
        plt.figure()
        ys = [df[c].to_numpy() for c in count_cols]
        labels = [c.replace("count_", "") for c in count_cols]
        plt.stackplot(x, ys, labels=labels)
        plt.xlabel("frame_idx")
        plt.ylabel("objects")
        plt.title("Detections per Class (Stacked)")
        plt.legend(loc="upper left", ncol=2, fontsize=8)
        savefig(plots_dir / "04_counts_per_class.png")

    # 05 - inference histogram
    plt.figure()
    plt.hist(df["inference_ms"].to_numpy(), bins=30)
    plt.xlabel("inference_ms")
    plt.ylabel("count")
    plt.title("Histogram: Inference Time (ms)")
    savefig(plots_dir / "05_inference_hist.png")

    # 06 - fps histogram
    fps_vals = fps_series.dropna().to_numpy()
    if len(fps_vals) > 0:
        plt.figure()
        plt.hist(fps_vals, bins=30)
        plt.xlabel("fps_inst")
        plt.ylabel("count")
        plt.title("Histogram: FPS (instant)")
        savefig(plots_dir / "06_fps_hist.png")

    # 07 - summary txt
    duration_s = None
    if df["timestamp_dt"].notna().any():
        t0 = df["timestamp_dt"].dropna().iloc[0]
        t1 = df["timestamp_dt"].dropna().iloc[-1]
        dur = float((t1 - t0).total_seconds())
        if dur >= 0:
            duration_s = dur

    n_frames = int(df["frame_idx"].max())
    inf_mean = float(df["inference_ms"].mean())
    inf_med = float(df["inference_ms"].median())
    fps_mean = float(fps_series.mean())
    fps_med2 = float(fps_series.median())
    clahe_mode = int(
        round(float(df["clahe_on"].mode().iloc[0]))) if "clahe_on" in df.columns else -1

    total_det = int(df["total_objects"].sum())
    zero_frames = int((df["total_objects"] == 0).sum())
    zero_pct = float(zero_frames / len(df) * 100.0)

    if duration_s is None or duration_s == 0:
        duration_s = float(
            n_frames / max(1e-6, fps_med2 if fps_med2 > 0 else 10.0))

    class_totals = {c.replace("count_", ""): int(
        df[c].sum()) for c in count_cols}

    summary_lines = []
    summary_lines.append(f"CSV: {csv_path}")
    summary_lines.append(f"Frames: {len(df)} (frame_idx max: {n_frames})")
    summary_lines.append(f"Duration_s (estimated): {duration_s:.3f}")
    summary_lines.append(f"CLAHE mode (dominant): {clahe_mode}  (1=ON,0=OFF)")
    summary_lines.append("")
    summary_lines.append(
        f"Inference ms: mean={inf_mean:.3f}, median={inf_med:.3f}")
    summary_lines.append(
        f"FPS inst: mean={fps_mean:.3f}, median={fps_med2:.3f}")
    summary_lines.append("")
    summary_lines.append(f"Total detections (sum total_objects): {total_det}")
    summary_lines.append(
        f"Frames with 0 detection: {zero_frames} ({zero_pct:.2f}%)")
    if class_totals:
        summary_lines.append("")
        summary_lines.append("Detections per class (total over session):")
        for k, v in sorted(class_totals.items(), key=lambda kv: kv[1], reverse=True):
            summary_lines.append(f"  - {k}: {v}")

    (plots_dir / "07_summary.txt").write_text("\n".join(summary_lines), encoding="utf-8")

    QMessageBox.information(
        None,
        "Selesai",
        "Grafik & ringkasan berhasil dibuat.\n\n"
        f"Folder output:\n{plots_dir}"
    )


if __name__ == "__main__":
    main()
