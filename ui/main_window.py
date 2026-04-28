"""
ui/main_window.py
==================
Layer View: Jendela utama aplikasi Activity Scheduler.
Menampilkan tabel jadwal, toolbar filter, dan tombol aksi.
Berkomunikasi dengan Controller untuk semua operasi data.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLabel, QComboBox, QDateEdit,
    QMessageBox, QFrame, QSizePolicy, QMenuBar,
    QCheckBox, QSpacerItem, QAbstractItemView, QMenu
)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QColor, QFont, QAction, QIcon

from controllers.activity_controller import ActivityController
from ui.activity_dialog import ActivityDialog

# ── Identitas Mahasiswa ──
NAMA_MAHASISWA = "Lalu Ahmad Purwadi"
NIM_MAHASISWA  = "F1D02310115"
APP_VERSION    = "1.0.0"


class MainWindow(QMainWindow):
    """
    Jendela utama aplikasi.
    Mengelola tampilan tabel jadwal dan interaksi pengguna.
    """

    # Mapping kolom tabel
    KOLOM = ["ID", "Aktivitas", "Kategori", "Tanggal",
             "Mulai", "Selesai", "Prioritas", "Lokasi"]

    # Warna prioritas
    WARNA_PRIORITAS = {
        "Tinggi":  QColor("#FFEBEE"),   # merah muda
        "Sedang":  QColor("#FFF9E6"),   # kuning muda
        "Rendah":  QColor("#E8F5E9"),   # hijau muda
    }
    TEKS_PRIORITAS = {
        "Tinggi":  QColor("#C62828"),
        "Sedang":  QColor("#F57F17"),
        "Rendah":  QColor("#2E7D32"),
    }

    def __init__(self):
        super().__init__()
        self.controller = ActivityController()
        self._setup_ui()
        self._setup_menubar()
        self._setup_connections()
        self.muat_data()

    # ══════════════════════════════════════════════
    #  SETUP UI
    # ══════════════════════════════════════════════
    def _setup_ui(self):
        self.setWindowTitle("Activity Scheduler — Penjadwalan Aktivitas")
        self.setMinimumSize(1000, 680)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # ── Header Banner ──
        root.addWidget(self._buat_header())

        # ── Konten Utama ──
        konten = QWidget()
        konten.setObjectName("kontenArea")
        konten_layout = QVBoxLayout(konten)
        konten_layout.setSpacing(16)
        konten_layout.setContentsMargins(24, 20, 24, 20)

        konten_layout.addWidget(self._buat_toolbar())
        konten_layout.addWidget(self._buat_tabel())
        konten_layout.addWidget(self._buat_footer())

        root.addWidget(konten)

    def _buat_header(self) -> QWidget:
        """Membuat header banner aplikasi."""
        header = QFrame()
        header.setObjectName("headerBanner")
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        # Kiri: judul aplikasi
        kiri = QVBoxLayout()
        kiri.setSpacing(2)

        lbl_app = QLabel("📅  Activity Scheduler")
        lbl_app.setObjectName("headerAppName")

        lbl_tagline = QLabel("Kelola aktivitas harianmu dengan mudah dan terstruktur")
        lbl_tagline.setObjectName("headerTagline")

        kiri.addWidget(lbl_app)
        kiri.addWidget(lbl_tagline)

        # Kanan: identitas mahasiswa
        kanan = QVBoxLayout()
        kanan.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        kanan.setSpacing(2)

        lbl_nama = QLabel(f"👤 {NAMA_MAHASISWA}")
        lbl_nama.setObjectName("headerNama")
        lbl_nama.setAlignment(Qt.AlignRight)

        lbl_nim = QLabel(f"🆔 NIM: {NIM_MAHASISWA}")
        lbl_nim.setObjectName("headerNim")
        lbl_nim.setAlignment(Qt.AlignRight)

        kanan.addWidget(lbl_nama)
        kanan.addWidget(lbl_nim)

        layout.addLayout(kiri)
        layout.addStretch()
        layout.addLayout(kanan)

        return header

    def _buat_toolbar(self) -> QWidget:
        """Membuat toolbar filter dan tombol aksi."""
        toolbar = QFrame()
        toolbar.setObjectName("toolbar")

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # ── Filter Tanggal ──
        lbl_tgl = QLabel("📆 Tanggal:")
        lbl_tgl.setObjectName("labelFilter")

        self.filter_tanggal = QDateEdit()
        self.filter_tanggal.setDate(QDate.currentDate())
        self.filter_tanggal.setCalendarPopup(True)
        self.filter_tanggal.setDisplayFormat("dd MMM yyyy")
        self.filter_tanggal.setObjectName("filterInput")
        self.filter_tanggal.setFixedWidth(150)

        self.cb_filter_tgl = QCheckBox("Aktifkan")
        self.cb_filter_tgl.setObjectName("checkFilter")

        # ── Filter Kategori ──
        lbl_kat = QLabel("🏷️ Kategori:")
        lbl_kat.setObjectName("labelFilter")

        self.filter_kategori = QComboBox()
        self.filter_kategori.addItem("Semua")
        self.filter_kategori.addItems(self.controller.get_kategori_list())
        self.filter_kategori.setObjectName("filterInput")
        self.filter_kategori.setFixedWidth(130)

        # ── Tombol Filter ──
        self.btn_filter = QPushButton("🔍 Filter")
        self.btn_filter.setObjectName("btnFilter")
        self.btn_filter.setFixedHeight(36)

        self.btn_reset = QPushButton("↺ Reset")
        self.btn_reset.setObjectName("btnReset")
        self.btn_reset.setFixedHeight(36)

        layout.addWidget(lbl_tgl)
        layout.addWidget(self.filter_tanggal)
        layout.addWidget(self.cb_filter_tgl)
        layout.addWidget(lbl_kat)
        layout.addWidget(self.filter_kategori)
        layout.addWidget(self.btn_filter)
        layout.addWidget(self.btn_reset)
        layout.addStretch()

        # ── Tombol Aksi CRUD ──
        self.btn_tambah = QPushButton("➕ Tambah")
        self.btn_tambah.setObjectName("btnTambah")
        self.btn_tambah.setFixedHeight(40)

        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.setFixedHeight(40)
        self.btn_edit.setEnabled(False)

        self.btn_hapus = QPushButton("🗑️ Hapus")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_hapus.setFixedHeight(40)
        self.btn_hapus.setEnabled(False)

        layout.addWidget(self.btn_tambah)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_hapus)

        return toolbar

    def _buat_tabel(self) -> QTableWidget:
        """Membuat widget tabel untuk menampilkan data aktivitas."""
        self.tabel = QTableWidget()
        self.tabel.setObjectName("tabelAktivitas")
        self.tabel.setColumnCount(len(self.KOLOM))
        self.tabel.setHorizontalHeaderLabels(self.KOLOM)

        # Sembunyikan kolom ID (index 0)
        self.tabel.setColumnHidden(0, True)

        # Pengaturan tabel
        header = self.tabel.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)   # Nama Aktivitas
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        self.tabel.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabel.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabel.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabel.setAlternatingRowColors(False)  # Kita handle manual via prioritas
        self.tabel.verticalHeader().setVisible(False)
        self.tabel.setShowGrid(True)
        self.tabel.setSortingEnabled(True)

        return self.tabel

    def _buat_footer(self) -> QWidget:
        """Membuat status bar bawah."""
        footer = QFrame()
        footer.setObjectName("footerBar")

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(8, 6, 8, 6)

        self.lbl_status = QLabel("Siap.")
        self.lbl_status.setObjectName("labelStatus")

        self.lbl_jumlah = QLabel("Total: 0 aktivitas")
        self.lbl_jumlah.setObjectName("labelJumlah")

        # Legend warna prioritas
        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(16)

        for label, warna in [("🔴 Tinggi", "#FFCDD2"), ("🟡 Sedang", "#FFF9C4"), ("🟢 Rendah", "#C8E6C9")]:
            badge = QLabel(label)
            badge.setObjectName("legendBadge")
            badge.setStyleSheet(f"background:{warna}; border-radius:4px; padding:2px 8px;")
            legend_layout.addWidget(badge)

        layout.addWidget(self.lbl_status)
        layout.addStretch()
        layout.addLayout(legend_layout)
        layout.addSpacing(16)
        layout.addWidget(self.lbl_jumlah)

        return footer

    def _setup_menubar(self):
        """Membuat menu bar dengan menu Tentang."""
        menubar = self.menuBar()

        # Menu File
        menu_file = menubar.addMenu("&File")
        aksi_keluar = QAction("&Keluar", self)
        aksi_keluar.setShortcut("Ctrl+Q")
        aksi_keluar.triggered.connect(self.close)
        menu_file.addAction(aksi_keluar)

        # Menu Tentang
        menu_tentang = menubar.addMenu("&Tentang")
        aksi_tentang = QAction("ℹ️ Tentang Aplikasi", self)
        aksi_tentang.triggered.connect(self._show_tentang)
        menu_tentang.addAction(aksi_tentang)

    # ══════════════════════════════════════════════
    #  SIGNALS & SLOTS
    # ══════════════════════════════════════════════
    def _setup_connections(self):
        """Menghubungkan semua sinyal ke slot-nya."""
        self.btn_tambah.clicked.connect(self._on_tambah)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_hapus.clicked.connect(self._on_hapus)
        self.btn_filter.clicked.connect(self.muat_data)
        self.btn_reset.clicked.connect(self._on_reset_filter)
        self.tabel.itemSelectionChanged.connect(self._on_seleksi_berubah)
        self.tabel.doubleClicked.connect(self._on_edit)  # Double click = edit

    def _on_seleksi_berubah(self):
        """Slot: aktifkan tombol Edit & Hapus saat baris dipilih."""
        ada_seleksi = len(self.tabel.selectedRows()) > 0 if hasattr(self.tabel, 'selectedRows') else bool(self.tabel.currentRow() >= 0)
        terpilih = self.tabel.currentRow() >= 0
        self.btn_edit.setEnabled(terpilih)
        self.btn_hapus.setEnabled(terpilih)

    def _on_tambah(self):
        """Slot: membuka dialog tambah aktivitas."""
        dialog = ActivityDialog(
            parent=self,
            kategori_list=self.controller.get_kategori_list()
        )
        if dialog.exec():
            data = dialog.get_data()
            sukses, pesan = self.controller.tambah(data)
            if sukses:
                self.muat_data()
                self._set_status(f"✅ {pesan}")
            else:
                QMessageBox.warning(self, "Gagal Menyimpan", pesan)

    def _on_edit(self):
        """Slot: membuka dialog edit aktivitas yang dipilih."""
        activity_id = self._get_id_terpilih()
        if not activity_id:
            return

        data_lama = self.controller.get_by_id(activity_id)
        if not data_lama:
            QMessageBox.warning(self, "Error", "Data tidak ditemukan.")
            return

        dialog = ActivityDialog(
            parent=self,
            data=data_lama,
            kategori_list=self.controller.get_kategori_list()
        )
        if dialog.exec():
            data_baru = dialog.get_data()
            sukses, pesan = self.controller.edit(activity_id, data_baru)
            if sukses:
                self.muat_data()
                self._set_status(f"✏️ {pesan}")
            else:
                QMessageBox.warning(self, "Gagal Memperbarui", pesan)

    def _on_hapus(self):
        """Slot: konfirmasi dan hapus aktivitas yang dipilih."""
        activity_id = self._get_id_terpilih()
        if not activity_id:
            return

        # Ambil nama aktivitas untuk konfirmasi
        baris = self.tabel.currentRow()
        nama = self.tabel.item(baris, 1).text() if self.tabel.item(baris, 1) else "ini"

        konfirmasi = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah kamu yakin ingin menghapus aktivitas:\n\n"
            f"  📌 {nama}\n\nTindakan ini tidak bisa dibatalkan.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            sukses, pesan = self.controller.hapus(activity_id)
            if sukses:
                self.muat_data()
                self._set_status(f"🗑️ {pesan}")
            else:
                QMessageBox.warning(self, "Gagal Menghapus", pesan)

    def _on_reset_filter(self):
        """Slot: reset semua filter ke default."""
        self.filter_tanggal.setDate(QDate.currentDate())
        self.filter_kategori.setCurrentIndex(0)
        self.cb_filter_tgl.setChecked(False)
        self.muat_data()
        self._set_status("Filter direset.")

    def _show_tentang(self):
        """Slot: menampilkan dialog Tentang Aplikasi."""
        QMessageBox.information(
            self, "Tentang Aplikasi",
            f"<h3>📅 Activity Scheduler</h3>"
            f"<p>Versi {APP_VERSION}</p>"
            f"<p>Aplikasi manajemen jadwal aktivitas harian yang membantu "
            f"pengguna mencatat, mengatur, dan memantau kegiatan mereka "
            f"secara terstruktur dan efisien.</p>"
            f"<hr>"
            f"<p><b>Dibuat oleh:</b> {NAMA_MAHASISWA}<br>"
            f"<b>NIM:</b> {NIM_MAHASISWA}</p>"
            f"<p><b>Teknologi:</b> Python · PySide6 · SQLite</p>"
            f"<p><b>Arsitektur:</b> MVC (Model-View-Controller)</p>"
        )

    # ══════════════════════════════════════════════
    #  DATA LOADING
    # ══════════════════════════════════════════════
    def muat_data(self):
        """Memuat data dari database dan menampilkannya di tabel."""
        # Tentukan filter
        filter_tgl = None
        if self.cb_filter_tgl.isChecked():
            filter_tgl = self.filter_tanggal.date().toString("yyyy-MM-dd")

        filter_kat = self.filter_kategori.currentText()

        data_list = self.controller.get_semua(
            filter_tanggal=filter_tgl,
            filter_kategori=filter_kat
        )

        self.tabel.setSortingEnabled(False)
        self.tabel.setRowCount(0)

        hari_ini = QDate.currentDate().toString("yyyy-MM-dd")

        for baris_idx, aktivitas in enumerate(data_list):
            self.tabel.insertRow(baris_idx)

            nilai = [
                str(aktivitas["id"]),
                aktivitas["nama"],
                aktivitas["kategori"],
                aktivitas["tanggal"],
                aktivitas["waktu_mulai"],
                aktivitas["waktu_selesai"],
                aktivitas["prioritas"],
                aktivitas.get("lokasi") or "-",
            ]

            prioritas = aktivitas["prioritas"]
            warna_bg = self.WARNA_PRIORITAS.get(prioritas, QColor("#FFFFFF"))
            warna_fg = self.TEKS_PRIORITAS.get(prioritas, QColor("#333333"))
            adalah_hari_ini = aktivitas["tanggal"] == hari_ini

            for kol_idx, teks in enumerate(nilai):
                item = QTableWidgetItem(teks)
                item.setTextAlignment(Qt.AlignCenter)

                # Warna baris berdasarkan prioritas
                item.setBackground(warna_bg)

                # Teks prioritas diberi warna
                if kol_idx == 6:
                    item.setForeground(warna_fg)
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)

                # Highlight hari ini dengan border
                if adalah_hari_ini:
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                self.tabel.setItem(baris_idx, kol_idx, item)

        self.tabel.setSortingEnabled(True)
        self.lbl_jumlah.setText(f"Total: {len(data_list)} aktivitas")
        self.btn_edit.setEnabled(False)
        self.btn_hapus.setEnabled(False)

    # ══════════════════════════════════════════════
    #  HELPER
    # ══════════════════════════════════════════════
    def _get_id_terpilih(self) -> int | None:
        """Mengambil ID dari baris yang dipilih di tabel."""
        baris = self.tabel.currentRow()
        if baris < 0:
            return None
        item = self.tabel.item(baris, 0)  # Kolom ID (tersembunyi)
        if not item:
            return None
        try:
            return int(item.text())
        except ValueError:
            return None

    def _set_status(self, pesan: str):
        """Memperbarui label status di footer."""
        self.lbl_status.setText(pesan)

