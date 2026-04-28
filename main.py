"""
main.py
========
Entry point aplikasi Activity Scheduler.
Bertanggung jawab untuk:
- Inisialisasi QApplication
- Memuat stylesheet eksternal (.qss)
- Menampilkan MainWindow

Alur Arsitektur:
    main.py
       │
       ▼
    MainWindow (View)
       │   ← sinyal / event pengguna
       ▼
    ActivityController (Controller)
       │   ← panggil operasi data
       ▼
    DatabaseManager (Model)
       │   ← query SQLite
       ▼
    activity_scheduler.db
"""

import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# Tambahkan root project ke sys.path agar import antar modul berjalan
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def load_stylesheet(app: QApplication) -> None:
    """Memuat file QSS eksternal dan menerapkannya ke aplikasi."""
    qss_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "styles", "style.qss"
    )
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
        print(f"[OK] Stylesheet dimuat dari: {qss_path}")
    else:
        print(f"[PERINGATAN] File stylesheet tidak ditemukan: {qss_path}")


def main():
    # Aktifkan High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Activity Scheduler")
    app.setOrganizationName("Pemrograman Visual")

    # Terapkan stylesheet eksternal
    load_stylesheet(app)

    # Tampilkan jendela utama
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
