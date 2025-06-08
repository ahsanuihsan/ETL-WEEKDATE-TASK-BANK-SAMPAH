import streamlit as st

# --- Class UMKMSystem (Query 1, 2, 3) ---
class UMKMSystem:
    def __init__(self, nama_umkm):
        self.nama_umkm = nama_umkm
        self.anggota = []
        self.dana_pinjaman = 50_000_000  # Rp50 juta

    def tambah_anggota(self, nama, jumlah_pinjaman):
        anggota = {"nama": nama, "pinjaman": jumlah_pinjaman}
        self.anggota.append(anggota)
        return f"Anggota **{nama}** ditambahkan dengan pinjaman Rp{jumlah_pinjaman:,}"

    def hitung_pengembalian(self, nama, tahun):
        for anggota in self.anggota:
            if anggota["nama"] == nama:
                bunga = anggota["pinjaman"] * 0.05 * tahun
                total = anggota["pinjaman"] + bunga
                return f"Pengembalian untuk **{nama}** setelah **{tahun}** tahun: **Rp{total:,.2f}**"
        return f"Anggota **{nama}** tidak ditemukan."

# --- Class Koperasi (Query 4, 5, 6) ---
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
        return f"Transaksi **{jenis_transaksi.capitalize()}** Rp{jumlah:,} untuk **{nama}** dicatat."

    def hitung_keuntungan(self):
        total_jual = 0
        total_beli = 0
        for transaksi in self.transaksi:
            if transaksi["jenis"].lower() == "jual":
                total_jual += transaksi["jumlah"]
            elif transaksi["jenis"].lower() == "beli":
                total_beli += transaksi["jumlah"]
        keuntungan = total_jual - total_beli
        return f"Keuntungan koperasi: **Rp{keuntungan:,}**"

# --- Class BankSampah (Query 7, 8, 9, 10) ---
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
            return f"**{jumlah_kg} kg** **{jenis_sampah}** dari **{nama}** dicatat."
        else:
            return f"Jenis sampah **{jenis_sampah}** tidak dikenal."

    def hitung_nilai_tukar(self, nama):
        total_nilai = 0
        for jenis_sampah, data in self.data_sampah.items():
            jumlah_kg = data["jumlah_kg"].get(nama, 0)
            nilai = jumlah_kg * data["nilai_tukar"]
            total_nilai += nilai
        return f"Nilai tukar sampah untuk **{nama}**: **Rp{total_nilai:,}**"

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

# --- Streamlit App ---

st.set_page_config(
    page_title="Sistem Revolusi Komunitas",
    page_icon="🌍",
    layout="wide"
)

st.title("🚀 Revolusi Komunitas: Sistem Terintegrasi UMKM, Koperasi, & Bank Sampah")
st.markdown("---")
st.write("Aplikasi demo ini menunjukkan fungsionalitas inti dari sistem pengelolaan terpadu untuk UMKM, Koperasi, dan Bank Sampah. Mari kita mulai!")

# Initialize objects in session state
if 'umkm_system' not in st.session_state:
    st.session_state.umkm_system = None
if 'koperasi_system' not in st.session_state:
    st.session_state.koperasi_system = None
if 'bank_sampah_system' not in st.session_state:
    st.session_state.bank_sampah_system = None
if 'anggota_list' not in st.session_state:
    st.session_state.anggota_list = []

# Sidebar for initial setup
with st.sidebar:
    st.header("Konfigurasi Sistem")
    nama_umkm_input = st.text_input("Nama Sistem/Komunitas:", "Desa Maju Bersama")

    if st.button("Mulai Sistem"):
        st.session_state.umkm_system = UMKMSystem(nama_umkm_input)
        st.session_state.koperasi_system = Koperasi(nama_umkm_input)
        st.session_state.bank_sampah_system = BankSampah(nama_umkm_input)
        st.session_state.anggota_list = [] # Reset anggota list
        st.success(f"Sistem **{nama_umkm_input}** berhasil dimulai!")
        st.toast("Sistem dimulai! Silakan tambahkan anggota.", icon="✅")


if st.session_state.umkm_system is None:
    st.info("Silakan mulai sistem dari sidebar di kiri.")
else:
    st.header(f"Sistem Aktif: {st.session_state.umkm_system.nama_umkm}")
    st.markdown("---")

    # --- Bagian UMKM ---
    st.subheader("💼 Pengelolaan UMKM")
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Tambah Anggota & Pinjaman")
        anggota_nama = st.text_input("Nama Anggota UMKM:", key="anggota_nama_umkm")
        anggota_pinjaman = st.number_input("Jumlah Pinjaman (Rp):", min_value=0, value=0, step=1000000, key="anggota_pinjaman_umkm")
        if st.button("Tambah Anggota UMKM"):
            if anggota_nama and anggota_pinjaman > 0:
                result = st.session_state.umkm_system.tambah_anggota(anggota_nama, anggota_pinjaman)
                st.session_state.koperasi_system.tambah_anggota(anggota_nama, anggota_pinjaman) # Add to koperasi too
                st.session_state.bank_sampah_system.tambah_anggota(anggota_nama, anggota_pinjaman) # Add to bank sampah too
                st.session_state.anggota_list.append(anggota_nama)
                st.success(result)
            else:
                st.warning("Nama anggota dan jumlah pinjaman tidak boleh kosong.")

    with col2:
        st.write("#### Hitung Pengembalian Pinjaman")
        if st.session_state.anggota_list:
            selected_anggota_umkm = st.selectbox("Pilih Anggota:", [""] + list(set(st.session_state.anggota_list)), key="select_anggota_umkm")
            tahun_pengembalian = st.number_input("Jumlah Tahun Pengembalian:", min_value=1, value=1, step=1, key="tahun_pengembalian_umkm")
            if st.button("Hitung Pengembalian"):
                if selected_anggota_umkm:
                    result = st.session_state.umkm_system.hitung_pengembalian(selected_anggota_umkm, tahun_pengembalian)
                    st.info(result)
                else:
                    st.warning("Silakan pilih anggota.")
        else:
            st.info("Tambahkan anggota terlebih dahulu untuk melihat opsi.")

    st.markdown("---")

    # --- Bagian Koperasi ---
    st.subheader("🤝 Pengelolaan Koperasi")
    col3, col4 = st.columns(2)

    with col3:
        st.write("#### Catat Transaksi Koperasi")
        if st.session_state.anggota_list:
            selected_anggota_koperasi = st.selectbox("Pilih Anggota:", [""] + list(set(st.session_state.anggota_list)), key="select_anggota_koperasi")
            jenis_transaksi = st.radio("Jenis Transaksi:", ("Beli", "Jual"), key="jenis_transaksi_koperasi")
            jumlah_transaksi = st.number_input("Jumlah Transaksi (Rp):", min_value=0, value=0, step=100000, key="jumlah_transaksi_koperasi")
            if st.button("Catat Transaksi"):
                if selected_anggota_koperasi and jumlah_transaksi > 0:
                    result = st.session_state.koperasi_system.catat_transaksi(selected_anggota_koperasi, jenis_transaksi.lower(), jumlah_transaksi)
                    st.success(result)
                else:
                    st.warning("Pilih anggota dan masukkan jumlah transaksi.")
        else:
            st.info("Tambahkan anggota terlebih dahulu untuk melihat opsi.")

    with col4:
        st.write("#### Keuntungan Koperasi")
        if st.button("Hitung Keuntungan Koperasi"):
            result = st.session_state.koperasi_system.hitung_keuntungan()
            st.metric(label="Total Keuntungan", value=result.split(': ')[1])
            st.success(result)
        st.markdown("Jumlah Transaksi Koperasi:")
        if st.session_state.koperasi_system.transaksi:
            for i, tx in enumerate(st.session_state.koperasi_system.transaksi):
                st.write(f"- {tx['nama']} ({tx['jenis'].capitalize()}): Rp{tx['jumlah']:,}")
        else:
            st.info("Belum ada transaksi dicatat.")

    st.markdown("---")

    # --- Bagian Bank Sampah ---
    st.subheader("♻️ Pengelolaan Bank Sampah")
    col5, col6 = st.columns(2)

    with col5:
        st.write("#### Catat Sampah Anggota")
        if st.session_state.anggota_list:
            selected_anggota_sampah = st.selectbox("Pilih Anggota:", [""] + list(set(st.session_state.anggota_list)), key="select_anggota_sampah")
            jenis_sampah = st.radio("Jenis Sampah:", ("plastik", "kertas"), key="jenis_sampah")
            jumlah_kg_sampah = st.number_input("Jumlah Sampah (kg):", min_value=0.0, value=0.0, step=0.1, format="%.1f", key="jumlah_kg_sampah")
            if st.button("Catat Sampah"):
                if selected_anggota_sampah and jumlah_kg_sampah > 0:
                    result = st.session_state.bank_sampah_system.catat_sampah(selected_anggota_sampah, jenis_sampah, jumlah_kg_sampah)
                    st.success(result)
                else:
                    st.warning("Pilih anggota dan masukkan jumlah sampah.")
        else:
            st.info("Tambahkan anggota terlebih dahulu untuk melihat opsi.")

    with col6:
        st.write("#### Nilai Tukar & Edukasi Sampah")
        if st.session_state.anggota_list:
            selected_anggota_edukasi = st.selectbox("Pilih Anggota untuk Cek:", [""] + list(set(st.session_state.anggota_list)), key="select_anggota_edukasi")
            if st.button("Lihat Nilai Tukar & Pesan Edukasi"):
                if selected_anggota_edukasi:
                    nilai_tukar_result = st.session_state.bank_sampah_system.hitung_nilai_tukar(selected_anggota_edukasi)
                    pesan_edukasi_result = st.session_state.bank_sampah_system.pesan_edukasi(selected_anggota_edukasi)
                    st.success(nilai_tukar_result)
                    st.info(pesan_edukasi_result)
                else:
                    st.warning("Silakan pilih anggota.")
        else:
            st.info("Tambahkan anggota terlebih dahulu untuk melihat opsi.")

    st.markdown("---")
    st.subheader("Laporan Data Sistem")

    st.write("#### Anggota Terdaftar")
    if st.session_state.umkm_system.anggota:
        st.dataframe(st.session_state.umkm_system.anggota)
    else:
        st.info("Belum ada anggota terdaftar.")

    st.write("#### Data Sampah (Total per Jenis)")
    if any(data["jumlah_kg"] for data in st.session_state.bank_sampah_system.data_sampah.values()):
        # Flatten the data_sampah for easier display
        display_data = []
        for jenis, data in st.session_state.bank_sampah_system.data_sampah.items():
            for nama, kg in data["jumlah_kg"].items():
                display_data.append({
                    "Jenis Sampah": jenis.capitalize(),
                    "Anggota": nama,
                    "Jumlah (kg)": kg,
                    "Nilai Tukar per Kg": data["nilai_tukar"]
                })
        st.dataframe(display_data)
    else:
        st.info("Belum ada data sampah dicatat.")