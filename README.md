# Deteksi Anomali Diskon Penjualan

Program sederhana untuk studi kasus PT Maju Bersama. Perusahaan ingin menemukan transaksi penjualan yang berpotensi merugikan karena diskon berlebihan atau data transaksi yang tidak wajar.

## Cara kerja

Program membaca `sales_transactions.csv`, lalu menandai transaksi yang memenuhi satu atau lebih aturan berikut:

- Diskon lebih dari 50%.
- Nilai penjualan nol atau negatif.
- Kategori pelanggan kosong.

Aturan ini sengaja dibuat sederhana agar mudah dipahami dan dijelaskan untuk tugas kuliah. Program bukan model Machine Learning atau AI generatif. Kolom `is_anomaly` pada dataset dipakai sebagai label pembanding untuk menghitung hasil evaluasi.

## Isi proyek

| File | Keterangan |
|---|---|
| `anomaly_detection.py` | Program deteksi dan evaluasi anomali menggunakan Python standar |
| `sales_transactions.csv` | Data transaksi sintetis beserta label anomali |
| `README.md` | Dokumentasi proyek |

Dataset yang tersedia berisi 206 transaksi. Program akan membaca jumlah dan isi data langsung dari CSV.

Kolom utama dataset:

| Kolom | Keterangan |
|---|---|
| `transaction_id` | ID unik transaksi |
| `sales_amount` | Nilai penjualan |
| `discount_percentage` | Persentase diskon |
| `customer_category` | Kategori pelanggan |
| `product_category` | Kategori produk |
| `days_in_inventory` | Lama barang tersimpan di gudang |
| `is_anomaly` | Label pembanding: `1` anomali, `0` normal |

## Menjalankan program

Pastikan Python 3 sudah terpasang. Tidak perlu memasang library tambahan.

1. Buka terminal pada folder proyek.
2. Jalankan:

   ```bash
   python anomaly_detection.py
   ```

   Program otomatis menggunakan `sales_transactions.csv` yang berada di folder proyek.

3. Untuk menggunakan file CSV lain, berikan lokasinya sebagai argumen:

   ```bash
   python anomaly_detection.py path/to/data.csv
   ```

Program menampilkan jumlah transaksi, anomali yang terdeteksi, metrik evaluasi (accuracy, precision, dan recall), confusion matrix, serta alasan setiap transaksi ditandai.

## Catatan evaluasi

Hasil evaluasi bergantung pada kecocokan aturan sederhana di atas dengan label `is_anomaly` di CSV. Precision menunjukkan proporsi transaksi yang ditandai dan memang berlabel anomali, sedangkan recall menunjukkan proporsi anomali berlabel yang berhasil ditemukan. Aturan ini merupakan contoh pembelajaran, bukan pengganti pemeriksaan atau persetujuan manusia.

Pada dataset yang disertakan, program menemukan 65 anomali dari 206 transaksi. Hasil evaluasinya adalah accuracy, precision, dan recall sebesar 100% (TP=65, FP=0, TN=141, FN=0). Angka ini hanya menggambarkan kecocokan aturan dengan dataset sintetis yang tersedia; hasil tersebut tidak menjamin performa yang sama pada transaksi nyata.
