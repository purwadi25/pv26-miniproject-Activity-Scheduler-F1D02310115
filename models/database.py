"""
models/database.py
==================
Layer Model: Mengelola koneksi dan operasi database SQLite.
Bertanggung jawab atas:
- Inisialisasi database dan tabel
- Operasi CRUD (Create, Read, Update, Delete)
- Query filter dan sorting
"""

import sqlite3
import os


class DatabaseManager:
    """
    Kelas utama untuk mengelola database SQLite.
    Semua operasi data dilakukan melalui kelas ini.
    """

    def __init__(self, db_path="activity_scheduler.db"):
        # Simpan database di folder project
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, db_path)
        self._init_database()

    def _get_connection(self):
        """Membuat dan mengembalikan koneksi database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Agar hasil query bisa diakses seperti dict
        return conn

    def _init_database(self):
        """Inisialisasi tabel jika belum ada."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nama        TEXT NOT NULL,
                kategori    TEXT NOT NULL,
                tanggal     TEXT NOT NULL,
                waktu_mulai TEXT NOT NULL,
                waktu_selesai TEXT NOT NULL,
                prioritas   TEXT NOT NULL,
                deskripsi   TEXT,
                lokasi      TEXT,
                created_at  TEXT DEFAULT (datetime('now','localtime'))
            )
        """)
        conn.commit()
        conn.close()

    # ──────────────── CREATE ────────────────
    def tambah_aktivitas(self, data: dict) -> int:
        """
        Menambahkan aktivitas baru ke database.
        Returns: id baris yang baru dibuat
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO activities
                (nama, kategori, tanggal, waktu_mulai, waktu_selesai, prioritas, deskripsi, lokasi)
            VALUES
                (:nama, :kategori, :tanggal, :waktu_mulai, :waktu_selesai, :prioritas, :deskripsi, :lokasi)
        """, data)
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    # ──────────────── READ ────────────────
    def ambil_semua(self, filter_tanggal=None, filter_kategori=None,
                    sort_kolom="tanggal", sort_asc=True) -> list:
        """
        Mengambil semua aktivitas dengan opsi filter dan sorting.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM activities WHERE 1=1"
        params = []

        if filter_tanggal:
            query += " AND tanggal = ?"
            params.append(filter_tanggal)

        if filter_kategori and filter_kategori != "Semua":
            query += " AND kategori = ?"
            params.append(filter_kategori)

        arah = "ASC" if sort_asc else "DESC"
        query += f" ORDER BY {sort_kolom} {arah}"

        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows

    def ambil_by_id(self, activity_id: int) -> dict:
        """Mengambil satu aktivitas berdasarkan ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def ambil_kategori_list(self) -> list:
        """Mengambil daftar kategori yang tersedia."""
        return ["Kuliah", "Pribadi", "Kerja", "Olahraga", "Ibadah", "Lainnya"]

    # ──────────────── UPDATE ────────────────
    def update_aktivitas(self, activity_id: int, data: dict) -> bool:
        """Memperbarui data aktivitas berdasarkan ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE activities SET
                nama = :nama,
                kategori = :kategori,
                tanggal = :tanggal,
                waktu_mulai = :waktu_mulai,
                waktu_selesai = :waktu_selesai,
                prioritas = :prioritas,
                deskripsi = :deskripsi,
                lokasi = :lokasi
            WHERE id = :id
        """, {**data, "id": activity_id})
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    # ──────────────── DELETE ────────────────
    def hapus_aktivitas(self, activity_id: int) -> bool:
        """Menghapus aktivitas berdasarkan ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

