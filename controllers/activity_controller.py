
from models.database import DatabaseManager


class ActivityController:
    """
    Controller untuk mengelola logika bisnis aktivitas.
    View hanya berinteraksi dengan Controller, bukan langsung ke Database.
    """

    def __init__(self):
        self.db = DatabaseManager()

    # ──────────────── VALIDASI ────────────────
    def validasi_input(self, data: dict) -> tuple[bool, str]:
        """
        Memvalidasi data input dari form.
        Returns: (True, "") jika valid, (False, pesan_error) jika tidak valid.
        """
        if not data.get("nama", "").strip():
            return False, "Nama aktivitas tidak boleh kosong."

        if not data.get("kategori", "").strip():
            return False, "Kategori harus dipilih."

        if not data.get("tanggal", "").strip():
            return False, "Tanggal harus diisi."

        if not data.get("waktu_mulai", "").strip():
            return False, "Waktu mulai harus diisi."

        if not data.get("waktu_selesai", "").strip():
            return False, "Waktu selesai harus diisi."

        if not data.get("prioritas", "").strip():
            return False, "Prioritas harus dipilih."

        # Validasi waktu: waktu_selesai harus setelah waktu_mulai
        if data["waktu_mulai"] >= data["waktu_selesai"]:
            return False, "Waktu selesai harus lebih besar dari waktu mulai."

        return True, ""

    # ──────────────── OPERASI CRUD ────────────────
    def tambah(self, data: dict) -> tuple[bool, str]:
        """
        Menambahkan aktivitas baru setelah validasi.
        Returns: (sukses, pesan)
        """
        valid, pesan = self.validasi_input(data)
        if not valid:
            return False, pesan

        try:
            self.db.tambah_aktivitas(data)
            return True, "Aktivitas berhasil ditambahkan."
        except Exception as e:
            return False, f"Gagal menyimpan: {str(e)}"

    def get_semua(self, filter_tanggal=None, filter_kategori=None,
                  sort_kolom="tanggal", sort_asc=True) -> list:
        """Mengambil semua data aktivitas dengan filter dan sorting."""
        return self.db.ambil_semua(filter_tanggal, filter_kategori, sort_kolom, sort_asc)

    def get_by_id(self, activity_id: int) -> dict:
        """Mengambil satu aktivitas berdasarkan ID."""
        return self.db.ambil_by_id(activity_id)

    def edit(self, activity_id: int, data: dict) -> tuple[bool, str]:
        """
        Memperbarui aktivitas setelah validasi.
        Returns: (sukses, pesan)
        """
        valid, pesan = self.validasi_input(data)
        if not valid:
            return False, pesan

        try:
            berhasil = self.db.update_aktivitas(activity_id, data)
            if berhasil:
                return True, "Aktivitas berhasil diperbarui."
            return False, "Aktivitas tidak ditemukan."
        except Exception as e:
            return False, f"Gagal memperbarui: {str(e)}"

    def hapus(self, activity_id: int) -> tuple[bool, str]:
        """
        Menghapus aktivitas berdasarkan ID.
        Returns: (sukses, pesan)
        """
        try:
            berhasil = self.db.hapus_aktivitas(activity_id)
            if berhasil:
                return True, "Aktivitas berhasil dihapus."
            return False, "Aktivitas tidak ditemukan."
        except Exception as e:
            return False, f"Gagal menghapus: {str(e)}"

    def get_kategori_list(self) -> list:
        """Mengambil daftar pilihan kategori."""
        return self.db.ambil_kategori_list()

