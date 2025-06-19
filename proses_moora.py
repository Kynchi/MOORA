import pandas as pd
import numpy as np
import os

def proses_moora(filepath):
    # Baca file (otomatis deteksi CSV/Excel)
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(filepath)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(filepath)
    else:
        return pd.DataFrame()  # File tidak didukung

    # Pastikan kolom yang dibutuhkan ada
    kolom_kriteria = ["Produktivitas", "Kedisiplinan", "Kualitas Kerja", "Kerja Sama", "Inovasi"]
    if not all(k in df.columns for k in kolom_kriteria):
        return pd.DataFrame()

    # Bobot kriteria (ubah sesuai kebutuhan)
    bobot = np.array([0.30, 0.20, 0.25, 0.15, 0.10])

    # Normalisasi matriks keputusan
    X = df[kolom_kriteria].values.astype(float)
    pembagi = np.sqrt((X**2).sum(axis=0))
    X_norm = X / pembagi

    # Hitung nilai optimasi (semua kriteria benefit)
    nilai_optimasi = (X_norm * bobot).sum(axis=1)

    # Buat DataFrame hasil
    df_hasil = pd.DataFrame({
        "Pegawai": df["Pegawai"] if "Pegawai" in df.columns else df.index + 1,
        "Nilai MOORA": nilai_optimasi
    })
    df_hasil["Ranking"] = df_hasil["Nilai MOORA"].rank(ascending=False, method="min").astype(int)
    df_hasil = df_hasil.sort_values("Ranking").reset_index(drop=True)


    return df_hasil