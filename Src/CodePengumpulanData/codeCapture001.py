#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import cv2
from pathlib import Path
from datetime import datetime

from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QComboBox, QLineEdit
)

# ==============================================================
# BASE PATH (KONSISTEN TESIS 2)
# ==============================================================
BASE_DIR = Path(__file__).resolve().parent

CAPTURE_DIR = (
    BASE_DIR
    / ".."
    / ".."
    / "Data"
    / "DataTesting"
    / "Input"
    / "HasilCaptureCamera"
).resolve()

CAPTURE_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================
# Camera Thread
# ==============================================================


class CameraThread(QThread):
    frame_ready = Signal(object)
    fps_detected = Signal(float)

    def __init__(self, cam_index=0, width=1280, height=720):
        super().__init__()
        self.cam_index = cam_index
        self.width = width
        self.height = height
        self.running = False
        self.recording = False
        self.video_writer = None
        self.video_fps = 20

    def run(self):
        cap = cv2.VideoCapture(self.cam_index)
        if not cap.isOpened():
            print("❌ Kamera tidak bisa dibuka")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or fps > 120:
            fps = 20

        self.video_fps = fps
        self.fps_detected.emit(fps)

        self.running = True
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            self.frame_ready.emit(frame)

            if self.recording and self.video_writer:
                self.video_writer.write(self._crop720(frame))

            self.msleep(5)

        cap.release()
        if self.video_writer:
            self.video_writer.release()

    def stop(self):
        self.running = False
        self.wait(1000)

    def _crop720(self, frame):
        h, w = frame.shape[:2]
        t = 720
        x = max(0, (w - t) // 2)
        y = max(0, (h - t) // 2)
        crop = frame[y:y+t, x:x+t]
        return cv2.resize(crop, (t, t))

    def start_recording(self, path: Path):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(
            str(path), fourcc, float(self.video_fps), (720, 720)
        )
        if not self.video_writer.isOpened():
            raise RuntimeError("Gagal membuka VideoWriter")
        self.recording = True

    def stop_recording(self):
        self.recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None


# ==============================================================
# Main Window
# ==============================================================
class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Capture - Doris Juarsa")

        self.output_dir = CAPTURE_DIR

        # ================= UI =================
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(720, 720)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet(
            "background:#111; border:2px solid #444;")
        self.preview_label.setScaledContents(False)

        self.combo_camera = QComboBox()
        self.combo_camera.addItem("Select Camera...")
        self.btn_refresh = QPushButton("🔄")
        self.btn_photo = QPushButton("📸 Take Photo")
        self.btn_record = QPushButton("⏺ Start Recording")
        self.btn_stop = QPushButton("⏹ Stop Recording")
        self.btn_choose = QPushButton("📁 Folder")

        self.fps_label = QLineEdit("FPS: --")
        self.fps_label.setReadOnly(True)
        self.folder_line = QLineEdit(str(self.output_dir))
        self.folder_line.setReadOnly(True)

        cam_layout = QHBoxLayout()
        cam_layout.addWidget(self.combo_camera)
        cam_layout.addWidget(self.btn_refresh)
        cam_layout.addWidget(self.fps_label)

        ctrl_layout = QHBoxLayout()
        ctrl_layout.addWidget(self.btn_photo)
        ctrl_layout.addWidget(self.btn_record)
        ctrl_layout.addWidget(self.btn_stop)
        ctrl_layout.addWidget(self.btn_choose)

        layout = QVBoxLayout(self)
        layout.addLayout(cam_layout)
        layout.addWidget(self.preview_label, alignment=Qt.AlignCenter)
        layout.addLayout(ctrl_layout)
        layout.addWidget(self.folder_line)

        # ================= STATE =================
        self.thread = None
        self.current_frame = None

        # ================= SIGNAL =================
        self.btn_refresh.clicked.connect(self.refresh_cameras)
        self.combo_camera.currentIndexChanged.connect(self.change_camera)
        self.btn_photo.clicked.connect(self.take_photo)
        self.btn_record.clicked.connect(self.start_recording)
        self.btn_stop.clicked.connect(self.stop_recording)
        self.btn_choose.clicked.connect(self.choose_folder)

        self.btn_stop.setEnabled(False)
        self.refresh_cameras()

    # ==================================================
    # Camera Management
    # ==================================================
    def refresh_cameras(self):
        self.combo_camera.clear()
        self.combo_camera.addItem("Select Camera...")
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.combo_camera.addItem(f"Camera {i}", i)
                cap.release()

    def change_camera(self):
        cam_index = self.combo_camera.currentData()
        if cam_index is None:
            return

        if self.thread:
            self.thread.stop()

        self.thread = CameraThread(cam_index)
        self.thread.frame_ready.connect(self.on_frame)
        self.thread.fps_detected.connect(self.on_fps_detected)
        self.thread.start()

    # ==================================================
    # Frame Update (CENTER FIXED)
    # ==================================================
    @Slot(object)
    def on_frame(self, frame):
        self.current_frame = frame
        disp = self.thread._crop720(frame)

        rgb = cv2.cvtColor(disp, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qimg)
        pixmap = pixmap.scaled(
            self.preview_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.preview_label.setPixmap(pixmap)

    @Slot(float)
    def on_fps_detected(self, fps):
        self.fps_label.setText(f"FPS: {fps:.1f}")

    # ==================================================
    # Actions
    # ==================================================
    def _timestamp(self):
        return datetime.now().strftime("%y%m%d_%H%M_%S")

    def take_photo(self):
        if self.current_frame is None:
            return
        path = self.output_dir / f"{self._timestamp()}.jpg"
        cv2.imwrite(str(path), self.thread._crop720(self.current_frame))

    def start_recording(self):
        path = self.output_dir / f"{self._timestamp()}.mp4"
        self.thread.start_recording(path)
        self.btn_record.setEnabled(False)
        self.btn_stop.setEnabled(True)

    def stop_recording(self):
        self.thread.stop_recording()
        self.btn_record.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Choose folder", str(self.output_dir)
        )
        if folder:
            self.output_dir = Path(folder)
            self.folder_line.setText(str(self.output_dir))

    def closeEvent(self, e):
        if self.thread:
            self.thread.stop()
        e.accept()


# ==============================================================
# Run App
# ==============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CameraApp()
    w.setFixedSize(820, 880)
    w.show()
    sys.exit(app.exec())
