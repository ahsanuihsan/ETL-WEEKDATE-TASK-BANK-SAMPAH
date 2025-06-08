class UMKMSystem:
    def __init__(self, nama_umkm):
        self.nama_umkm = nama_umkm
        self.anggota = []
        self.dana_pinjaman = 50_000_000  # Rp50 juta

    def tambah_anggota(self, nama, jumlah_pinjaman):
        anggota = {"nama": nama, "pinjaman": jumlah_pinjaman}
        self.anggota.append(anggota)
        print(f"Anggota {nama} ditambahkan dengan pinjaman Rp{jumlah_pinjaman:,}")

    def hitung_pengembalian(self, nama, tahun):
        for anggota in self.anggota:
            if anggota["nama"] == nama:
                bunga = anggota["pinjaman"] * 0.05 * tahun  # Bunga 5% per tahun
                total = anggota["pinjaman"] + bunga
                return f"Pengembalian untuk {nama} setelah {tahun} tahun: Rp{total:,.2f}"
        return f"Anggota {nama} tidak ditemukan."

class Koperasi(UMKMSystem):
    def __init__(self, nama_umkm):
        super().__init__(nama_umkm)
        self.transaksi = []

    def catat_transaksi(self, nama, jenis_transaksi, jumlah):
        transaksi = {
            "nama": nama,
            "jenis": jenis_transaksi,
            "jumlah": jumlah
        }
        self.transaksi.append(transaksi)
        print(f"Transaksi {jenis_transaksi} Rp{jumlah:,} untuk {nama} dicatat.")

    def hitung_keuntungan(self):
        total_jual = 0
        total_beli = 0
        for transaksi in self.transaksi:
            if transaksi["jenis"].lower() == "jual":
                total_jual += transaksi["jumlah"]
            elif transaksi["jenis"].lower() == "beli":
                total_beli += transaksi["jumlah"]
        keuntungan = total_jual - total_beli
        return f"Keuntungan koperasi: Rp{keuntungan:,}"

class BankSampah(UMKMSystem):
    def __init__(self, nama_umkm):
        super().__init__(nama_umkm)
        self.data_sampah = {
            "plastik": {"nilai_tukar": 5000, "jumlah_kg": {}},
            "kertas": {"nilai_tukar": 2000, "jumlah_kg": {}}
        }

    def catat_sampah(self, nama, jenis_sampah, jumlah_kg):
        if jenis_sampah in self.data_sampah:
            if nama in self.data_sampah[jenis_sampah]["jumlah_kg"]:
                self.data_sampah[jenis_sampah]["jumlah_kg"][nama] += jumlah_kg
            else:
                self.data_sampah[jenis_sampah]["jumlah_kg"][nama] = jumlah_kg
            print(f"{jumlah_kg} kg {jenis_sampah} dari {nama} dicatat.")
        else:
            print(f"Jenis sampah {jenis_sampah} tidak dikenal.")

    def hitung_nilai_tukar(self, nama):
        total_nilai = 0
        for jenis_sampah, data in self.data_sampah.items():
            jumlah_kg = data["jumlah_kg"].get(nama, 0)
            nilai = jumlah_kg * data["nilai_tukar"]
            total_nilai += nilai
        return f"Nilai tukar sampah untuk {nama}: Rp{total_nilai:,}"

    def pesan_edukasi(self, nama):
        total_sampah = 0
        for jenis_sampah in self.data_sampah:
            total_sampah += self.data_sampah[jenis_sampah]["jumlah_kg"].get(nama, 0)
        
        if total_sampah > 50:
            return "Selamat! Anda telah membantu mengurangi sampah secara signifikan. Mari terus dukung daur ulang untuk bumi yang lebih hijau!"
        elif total_sampah > 20:
            return "Kerja bagus! Anda berkontribusi pada lingkungan yang lebih bersih. Ayo kumpulkan lebih banyak sampah untuk didaur ulang!"
        elif total_sampah > 0:
            return "Terima kasih telah berpartisipasi di bank sampah. Setiap kilogram sampah yang Anda kumpulkan membantu lingkungan!"
        else:
            return "Ayo mulai kumpulkan sampah untuk mendukung keberlanjutan lingkungan!"

# Program Utama
def main():
    print("=== Sistem Pengelolaan UMKM, Koperasi, dan Bank Sampah ===")
    
    # Input nama UMKM
    nama_umkm = input("Masukkan nama UMKM: ")
    
    # Membuat objek Koperasi dan BankSampah
    koperasi = Koperasi(nama_umkm)
    bank_sampah = BankSampah(nama_umkm)
    
    # Menambah anggota
    while True:
        nama = input("\nMasukkan nama anggota (atau 'selesai' untuk lanjut): ")
        if nama.lower() == 'selesai':
            break
        pinjaman = float(input("Masukkan jumlah pinjaman (Rp): "))
        koperasi.tambah_anggota(nama, pinjaman)
        bank_sampah.tambah_anggota(nama, pinjaman)
    
    # Menghitung pengembalian pinjaman
    nama = input("\nMasukkan nama anggota untuk cek pengembalian: ")
    tahun = int(input("Masukkan jumlah tahun: "))
    print(koperasi.hitung_pengembalian(nama, tahun))
    
    # Mencatat transaksi koperasi
    while True:
        nama = input("\nMasukkan nama anggota untuk transaksi (atau 'selesai' untuk lanjut): ")
        if nama.lower() == 'selesai':
            break
        jenis = input("Masukkan jenis transaksi (beli/jual): ")
        jumlah = float(input("Masukkan jumlah transaksi (Rp): "))
        koperasi.catat_transaksi(nama, jenis, jumlah)
    
    # Menghitung keuntungan koperasi
    print(koperasi.hitung_keuntungan())
    
    # Mencatat data sampah
    while True:
        nama = input("\nMasukkan nama anggota untuk sampah (atau 'selesai' untuk lanjut): ")
        if nama.lower() == 'selesai':
            break
        jenis_sampah = input("Masukkan jenis sampah (plastik/kertas): ")
        jumlah_kg = float(input("Masukkan jumlah sampah (kg): "))
        bank_sampah.catat_sampah(nama, jenis_sampah, jumlah_kg)
    
    # Menghitung nilai tukar dan pesan edukasi
    nama = input("\nMasukkan nama anggota untuk cek nilai tukar dan edukasi: ")
    print(bank_sampah.hitung_nilai_tukar(nama))
    print(bank_sampah.pesan_edukasi(nama))

if __name__ == "__main__":
    main()