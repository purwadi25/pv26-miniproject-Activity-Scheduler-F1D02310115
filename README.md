# 📅 Activity Scheduler

Aplikasi **Activity Scheduler** adalah aplikasi desktop berbasis GUI yang dibuat menggunakan **Python (PySide6)** untuk membantu pengguna mengelola jadwal aktivitas harian secara terstruktur.

---

## 👤 Informasi Mahasiswa

* **Nama:** Lalu Ahmad Purwadi
* **NIM:** F1D02310115
* **Mata Kuliah:** Pemrograman Visual

---

## 🎯 Deskripsi Aplikasi

Aplikasi ini digunakan untuk mencatat, mengatur, dan memantau aktivitas harian pengguna.
Pengguna dapat menambahkan, mengedit, menghapus, dan melihat daftar aktivitas dengan fitur filter berdasarkan tanggal dan kategori.

---

## ⚙️ Fitur Utama

* ✅ Tambah aktivitas baru
* ✅ Edit aktivitas
* ✅ Hapus aktivitas (dengan konfirmasi)
* ✅ Tampilkan data dalam tabel
* ✅ Filter berdasarkan tanggal dan kategori
* ✅ Validasi input data
* ✅ Penyimpanan data menggunakan SQLite (persisten)
* ✅ Menu "Tentang Aplikasi"
* ✅ Tampilan menggunakan styling QSS eksternal

---

## 🧱 Struktur Project (Separation of Concerns)

```
pv26-miniproject-Activity-Scheduler-F1D02310115/
│
├── main.py
├── README.md
│
├── controllers/
│   └── activity_controller.py
│
├── models/
│   └── database.py
│
├── ui/
│   ├── main_window.py
│   └── activity_dialog.py
│
├── styles/
│   └── style.qss
```

* **UI (View):** menampilkan tampilan aplikasi
* **Controller:** mengatur logika dan validasi
* **Model:** mengelola database SQLite
* **Style:** tampilan visual (QSS)

---

## 💾 Teknologi yang Digunakan

* Python
* PySide6 (GUI)
* SQLite (Database)
* QSS (Styling)

---

## ▶️ Cara Menjalankan Aplikasi

### 1. Install dependency

```bash
pip install PySide6
```

### 2. Jalankan aplikasi

```bash
python main.py
```

---

## 🗄️ Database

* Database menggunakan **SQLite**
* File database akan otomatis dibuat saat aplikasi pertama kali dijalankan:

```
activity_scheduler.db
```

---

## 🎥 Video Penjelasan

(Link YouTube akan ditambahkan di sini)

---

## 📄 Laporan

(File laporan PDF akan disertakan dalam repository)

---

## 📝 Catatan

Aplikasi ini dibuat sebagai tugas mini project mata kuliah Pemrograman Visual dengan menerapkan konsep:

* GUI Programming
* Database Integration
* Styling dengan QSS
* Arsitektur MVC (Separation of Concerns)
