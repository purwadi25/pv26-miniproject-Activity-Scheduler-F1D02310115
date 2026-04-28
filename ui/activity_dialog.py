"""
ui/activity_dialog.py
======================
Layer View: Dialog form untuk Tambah dan Edit aktivitas.
Menggunakan QDialog agar terpisah dari MainWindow.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QDateEdit, QTimeEdit,
    QTextEdit, QPushButton, QLabel, QFrame, QMessageBox
)
from PySide6.QtCore import QDate, QTime, Qt
from PySide6.QtGui import QFont


class ActivityDialog(QDialog):
    """
    Dialog form untuk tambah/edit aktivitas.
    Menerima data awal (edit mode) atau kosong (tambah mode).
    """

    def __init__(self, parent=None, data=None, kategori_list=None):
        super().__init__(parent)
        self.data = data  # None = mode tambah, ada isi = mode edit
        self.kategori_list = kategori_list or []
        self.result_data = None  # Akan diisi saat user klik Simpan

        self._setup_ui()
        self._setup_connections()

        # Jika mode edit, isi form dengan data yang ada
        if self.data:
            self._populate_form()

    def _setup_ui(self):
        """Membangun layout dan widget dialog."""
        mode = "Edit Aktivitas" if self.data else "Tambah Aktivitas Baru"
        self.setWindowTitle(mode)
        self.setMinimumWidth(480)
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # ── Header ──
        header = QLabel(f"📋 {mode}")
        header.setObjectName("dialogHeader")
        main_layout.addWidget(header)

        # ── Garis pemisah ──
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName("divider")
        main_layout.addWidget(line)

        # ── Form Layout ──
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Nama Aktivitas
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Contoh: Kuliah Pemrograman Visual")
        self.input_nama.setObjectName("formInput")
        form.addRow("Nama Aktivitas *", self.input_nama)

        # Kategori
        self.input_kategori = QComboBox()
        self.input_kategori.addItems(self.kategori_list)
        self.input_kategori.setObjectName("formInput")
        form.addRow("Kategori *", self.input_kategori)

        # Tanggal
        self.input_tanggal = QDateEdit()
        self.input_tanggal.setDate(QDate.currentDate())
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setDisplayFormat("yyyy-MM-dd")
        self.input_tanggal.setObjectName("formInput")
        form.addRow("Tanggal *", self.input_tanggal)

        # Waktu Mulai & Selesai (dalam satu baris)
        waktu_layout = QHBoxLayout()
        self.input_waktu_mulai = QTimeEdit()
        self.input_waktu_mulai.setTime(QTime(8, 0))
        self.input_waktu_mulai.setDisplayFormat("HH:mm")
        self.input_waktu_mulai.setObjectName("formInput")

        lbl_sd = QLabel("s/d")
        lbl_sd.setAlignment(Qt.AlignCenter)
        lbl_sd.setObjectName("labelSd")

        self.input_waktu_selesai = QTimeEdit()
        self.input_waktu_selesai.setTime(QTime(9, 0))
        self.input_waktu_selesai.setDisplayFormat("HH:mm")
        self.input_waktu_selesai.setObjectName("formInput")

        waktu_layout.addWidget(self.input_waktu_mulai)
        waktu_layout.addWidget(lbl_sd)
        waktu_layout.addWidget(self.input_waktu_selesai)
        form.addRow("Waktu *", waktu_layout)

        # Prioritas
        self.input_prioritas = QComboBox()
        self.input_prioritas.addItems(["🟢 Rendah", "🟡 Sedang", "🔴 Tinggi"])
        self.input_prioritas.setObjectName("formInput")
        form.addRow("Prioritas *", self.input_prioritas)

        # Lokasi (opsional)
        self.input_lokasi = QLineEdit()
        self.input_lokasi.setPlaceholderText("Contoh: Ruang D401, Zoom, dll.")
        self.input_lokasi.setObjectName("formInput")
        form.addRow("Lokasi", self.input_lokasi)

        # Deskripsi
        self.input_deskripsi = QTextEdit()
        self.input_deskripsi.setPlaceholderText("Catatan tambahan tentang aktivitas ini...")
        self.input_deskripsi.setObjectName("formTextArea")
        self.input_deskripsi.setMaximumHeight(100)
        form.addRow("Deskripsi", self.input_deskripsi)

        main_layout.addLayout(form)

        # ── Label wajib ──
        lbl_wajib = QLabel("* Field wajib diisi")
        lbl_wajib.setObjectName("labelWajib")
        main_layout.addWidget(lbl_wajib)

        # ── Tombol Aksi ──
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnBatal")
        self.btn_batal.setMinimumHeight(40)

        self.btn_simpan = QPushButton("💾 Simpan")
        self.btn_simpan.setObjectName("btnSimpan")
        self.btn_simpan.setMinimumHeight(40)
        self.btn_simpan.setDefault(True)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addWidget(self.btn_simpan)
        main_layout.addLayout(btn_layout)

    def _setup_connections(self):
        """Menghubungkan sinyal ke slot."""
        self.btn_simpan.clicked.connect(self._on_simpan)
        self.btn_batal.clicked.connect(self.reject)

    def _populate_form(self):
        """Mengisi form dengan data existing (mode edit)."""
        self.input_nama.setText(self.data.get("nama", ""))
        
        idx_kategori = self.input_kategori.findText(self.data.get("kategori", ""))
        if idx_kategori >= 0:
            self.input_kategori.setCurrentIndex(idx_kategori)

        tanggal = QDate.fromString(self.data.get("tanggal", ""), "yyyy-MM-dd")
        if tanggal.isValid():
            self.input_tanggal.setDate(tanggal)

        waktu_mulai = QTime.fromString(self.data.get("waktu_mulai", ""), "HH:mm")
        if waktu_mulai.isValid():
            self.input_waktu_mulai.setTime(waktu_mulai)

        waktu_selesai = QTime.fromString(self.data.get("waktu_selesai", ""), "HH:mm")
        if waktu_selesai.isValid():
            self.input_waktu_selesai.setTime(waktu_selesai)

        # Mapping prioritas ke index kombobox
        prioritas_map = {"Rendah": 0, "Sedang": 1, "Tinggi": 2}
        idx_prioritas = prioritas_map.get(self.data.get("prioritas", ""), 0)
        self.input_prioritas.setCurrentIndex(idx_prioritas)

        self.input_lokasi.setText(self.data.get("lokasi", "") or "")
        self.input_deskripsi.setPlainText(self.data.get("deskripsi", "") or "")

    def _on_simpan(self):
        """Slot: Mengumpulkan data form dan menyimpannya ke result_data."""
        # Ambil prioritas tanpa emoji
        prioritas_raw = self.input_prioritas.currentText()
        prioritas_clean = prioritas_raw.split(" ")[-1]  # "🟢 Rendah" → "Rendah"

        self.result_data = {
            "nama": self.input_nama.text().strip(),
            "kategori": self.input_kategori.currentText(),
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd"),
            "waktu_mulai": self.input_waktu_mulai.time().toString("HH:mm"),
            "waktu_selesai": self.input_waktu_selesai.time().toString("HH:mm"),
            "prioritas": prioritas_clean,
            "lokasi": self.input_lokasi.text().strip(),
            "deskripsi": self.input_deskripsi.toPlainText().strip(),
        }
        self.accept()

    def get_data(self) -> dict:
        """Mengembalikan data yang sudah diisi pengguna."""
        return self.result_data

