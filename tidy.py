"""
Script untuk merapikan file di folder Downloads
berdasarkan KATA KUNCI yang ada di nama file.

Cara pakai:
1. Sesuaikan TARGET_FOLDER di bawah (lokasi folder Downloads kamu)
2. Sesuaikan KATEGORI sesuai kebutuhan (tambah/kurangi kata kunci)
3. Jalankan: python rapikan_downloads.py
4. Script akan tanya konfirmasi dulu sebelum memindah file (mode aman)
"""

import os
import shutil
from pathlib import Path

# ============================================================
# 1. KONFIGURASI - ubah bagian ini sesuai kebutuhanmu
# ============================================================

# Lokasi folder yang mau dirapikan
TARGET_FOLDER = r"C:\Users\Lenovo\Downloads"

# Kategori: nama_folder_tujuan -> daftar kata kunci (huruf kecil semua)
# File akan dicek satu per satu, kata kunci pertama yang cocok dipakai.
KATEGORI = {
    "Skripsi": [
        "skripsi", "proposal_ta", "bab_", "metodologi", "indoroberta",
        "state_of_the_art", "sempro",
    ],
    "Project_Web": [
        "drawio", "arsitektur", "antarmuka", "flowchart", "aplikasi_web",
        "deteksi_ai", "googlea",
    ],
    "Installer": [
        "setup", "installer", "install_",
    ],
    "Source_Code": [
        # ekstensi kode tetap dicek lewat tipe file di bawah,
        # tapi kalau ada kata kunci khusus proyek bisa ditambah di sini
        "portfolio",
    ],
}

# Fallback berdasarkan EKSTENSI, dipakai kalau nama file tidak cocok
# dengan kata kunci kategori manapun di atas.
KATEGORI_BY_EXTENSION = {
    "Dokumen": [".pdf", ".doc", ".docx", ".txt"],
    "Gambar": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    "Source_Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp"],
    "Installer": [".exe", ".msi"],
    "Compressed": [".zip", ".rar", ".7z"],
}

# Folder untuk file yang tidak cocok kategori apapun
FOLDER_LAINNYA = "Lainnya"

# Mode simulasi dulu (True = cuma preview, tidak benar-benar pindah file)
DRY_RUN = False


# ============================================================
# 2. LOGIKA SCRIPT - tidak perlu diubah
# ============================================================

def tentukan_kategori(nama_file: str) -> str:
    nama_lower = nama_file.lower()

    # Cek berdasarkan kata kunci nama file dulu
    for folder_tujuan, kata_kunci_list in KATEGORI.items():
        for kata_kunci in kata_kunci_list:
            if kata_kunci in nama_lower:
                return folder_tujuan

    # Kalau tidak ketemu, cek berdasarkan ekstensi
    ekstensi = Path(nama_file).suffix.lower()
    for folder_tujuan, ekstensi_list in KATEGORI_BY_EXTENSION.items():
        if ekstensi in ekstensi_list:
            return folder_tujuan

    return FOLDER_LAINNYA


def rapikan_folder():
    target = Path(TARGET_FOLDER)

    if not target.exists():
        print(f"❌ Folder tidak ditemukan: {target}")
        return

    semua_file = [f for f in target.iterdir() if f.is_file()]

    if not semua_file:
        print("Tidak ada file untuk dirapikan.")
        return

    rencana = {}  # folder_tujuan -> list nama file
    for file_path in semua_file:
        kategori = tentukan_kategori(file_path.name)
        rencana.setdefault(kategori, []).append(file_path.name)

    # Tampilkan preview dulu
    print("=" * 60)
    print("PREVIEW PENGELOMPOKAN")
    print("=" * 60)
    for folder_tujuan, file_list in rencana.items():
        print(f"\n📁 {folder_tujuan}/  ({len(file_list)} file)")
        for nama in file_list:
            print(f"   - {nama}")

    print("\n" + "=" * 60)

    if DRY_RUN:
        print("⚠️  MODE SIMULASI (DRY_RUN = False).")
        print("Belum ada file yang dipindah. Ubah DRY_RUN = False di script")
        print("kalau hasil preview di atas sudah sesuai keinginanmu.")
        return

    konfirmasi = input("\nLanjutkan memindahkan file sesuai preview di atas? (y/n): ")
    if konfirmasi.strip().lower() != "y":
        print("Dibatalkan, tidak ada file yang dipindah.")
        return

    for folder_tujuan, file_list in rencana.items():
        folder_path = target / folder_tujuan
        folder_path.mkdir(exist_ok=True)
        for nama in file_list:
            sumber = target / nama
            tujuan = folder_path / nama
            # hindari overwrite kalau nama sudah ada di folder tujuan
            if tujuan.exists():
                tujuan = folder_path / f"{tujuan.stem}_copy{tujuan.suffix}"
            shutil.move(str(sumber), str(tujuan))
            print(f"✅ Dipindah: {nama} -> {folder_tujuan}/")

    print("\nSelesai merapikan file!")


if __name__ == "__main__":
    rapikan_folder()