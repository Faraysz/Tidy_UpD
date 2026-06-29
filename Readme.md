# Rapikan Downloads

Script Python sederhana untuk merapikan file-file yang menumpuk di satu folder (misalnya folder Downloads) dengan mengelompokkannya ke dalam subfolder, berdasarkan **kata kunci di nama file**.

## Kenapa Pakai Ini?

Folder Downloads biasanya jadi tempat numpuk segala jenis file — dokumen skripsi, file project, installer aplikasi, gambar, dan lain-lain — tanpa struktur yang jelas. Script ini membantu mengelompokkan file-file tersebut secara otomatis sesuai aturan yang kamu tentukan sendiri.

## Fitur

- Mengelompokkan file berdasarkan **kata kunci** pada nama file (contoh: `skripsi`, `drawio`, `setup`)
- Fallback ke pengelompokan berdasarkan **ekstensi file** jika tidak ada kata kunci yang cocok
- **Mode simulasi (dry run)** — menampilkan rencana pengelompokan dulu sebelum benar-benar memindahkan file apa pun
- Aman dari overwrite — kalau nama file sudah ada di folder tujuan, otomatis ditambahkan `_copy`
- Konfigurasi penuh ada di bagian atas file, tidak perlu mengubah logika inti

## Persyaratan

- Python 3.6 atau lebih baru ([download di sini](https://www.python.org/downloads/) kalau belum punya)
- Tidak ada library tambahan yang perlu di-install (hanya pakai modul bawaan Python: `os`, `shutil`, `pathlib`)

## Cara Pakai

### 1. Sesuaikan Konfigurasi

Buka `rapikan_downloads.py` dengan text editor, lalu sesuaikan bagian berikut:

**Lokasi folder yang mau dirapikan:**
```python
TARGET_FOLDER = r"C:\Users\Lenovo\Downloads"
```

**Kategori dan kata kunci:**
```python
KATEGORI = {
    "Skripsi": ["skripsi", "proposal_ta", "bab_", "metodologi"],
    "Project_Web": ["drawio", "arsitektur", "antarmuka", "flowchart"],
    "Installer": ["setup", "installer"],
    # tambahkan kategori dan kata kunci lain sesuai kebutuhan
}
```

> Kata kunci dicek dalam huruf kecil dan mencari kecocokan substring, jadi `bab_` akan cocok dengan `Bab_1_2_IndoRoBERTa.docx`.

Jika nama file tidak cocok dengan kata kunci apa pun, script akan memeriksa **ekstensi file** lewat `KATEGORI_BY_EXTENSION`. File yang tidak cocok kategori apa pun akan masuk ke folder `Lainnya`.

### 2. Jalankan dalam Mode Simulasi (Default)

```bash
python rapikan_downloads.py
```

Secara default, `DRY_RUN = True`, jadi script hanya akan **menampilkan preview** pengelompokan tanpa memindahkan file apa pun. Contoh output:

```
📁 Skripsi/  (4 file)
   - proposal_ta_E41230453.pdf
   - Bab_3_Metodologi_Penelitian.docx
   ...

📁 Project_Web/  (6 file)
   - Flowchart Alur Penggunaan Aplikasi.drawio
   ...
```

Periksa hasil preview ini dulu — pastikan pengelompokannya sudah sesuai keinginan.

### 3. Jalankan Pemindahan File Sungguhan

Setelah preview sesuai, ubah baris berikut menjadi `False`:

```python
DRY_RUN = False
```

Jalankan lagi:

```bash
python rapikan_downloads.py
```

Script akan menampilkan preview yang sama, lalu meminta konfirmasi:

```
Lanjutkan memindahkan file sesuai preview di atas? (y/n):
```

Ketik `y` dan tekan Enter untuk melanjutkan, atau `n` untuk membatalkan.

## Struktur Folder Setelah Dirapikan

Contoh hasil akhir:

```
Downloads/
├── Skripsi/
│   ├── proposal_ta_E41230453.pdf
│   └── Bab_3_Metodologi_Penelitian.docx
├── Project_Web/
│   ├── Flowchart Alur Penggunaan Aplikasi.drawio
│   └── arsitektur_sistem_deteksi_ai.png
├── Installer/
│   └── SpotifySetup.exe
├── Lainnya/
│   └── (file yang tidak cocok kategori apa pun)
```

## Catatan Keamanan

- Script **tidak akan pernah** menghapus file, hanya memindahkan (`shutil.move`)
- Selalu jalankan dalam mode `DRY_RUN = True` terlebih dahulu sebelum mengaktifkan pemindahan sungguhan
- Disarankan backup folder penting sebelum menjalankan script apa pun yang memindahkan banyak file sekaligus

## Kustomisasi Lanjutan

Ingin menambah kategori baru? Cukup tambahkan entri baru ke dictionary `KATEGORI`:

```python
KATEGORI = {
    "Skripsi": [...],
    "Project_Web": [...],
    "Kuliah": ["tugas", "uas", "uts", "praktikum"],  # kategori baru
}
```

Tidak perlu mengubah bagian logika (`tentukan_kategori`, `rapikan_folder`) — cukup ubah konfigurasi di bagian atas file.

## Pengembangan Selanjutnya

Kalau butuh versi yang berjalan otomatis di background (memantau folder dan memindahkan file baru secara real-time tanpa perlu dijalankan manual setiap kali), itu bisa dibuat sebagai script terpisah menggunakan library `watchdog`.