import streamlit as st
from datetime import datetime
from pages.const.fun import open_peminjaman, open_siswa, open_buku


def cari_info(info):
    for i in data:
        for x in data[i]['id']:
            for z in x:
                tanggal_kembali = datetime.strptime(x[str(z)]['tanggal_kembali'], '%d/%m/%Y').date()
                hari_ini = datetime.today().date()
                delta = hari_ini - tanggal_kembali
                if tanggal_kembali < hari_ini and info == "terlambat":
                    display(i, x, z, 'terlambat',
                            f""""⚠️ TERLAMBAT {delta.days} HARI!!
                            🗓 Tanggal Pengembalian = {x[str(z)]['tanggal_kembali']}""")
                elif tanggal_kembali == hari_ini and info == "today":
                    display(i, x, z, 'today',
                            f"Masa peminjaman berakhir hari ini. ({x[str(z)]['tanggal_kembali']})")
                elif tanggal_kembali > hari_ini and info == "masa_pinjam":
                    display(i, x, z, 'masa_pinjam',
                            f"""⏳ Dalam masa peminjaman.
                            Berakhir {delta.days * (-1)} hari lagi ({x[str(z)]['tanggal_kembali']}).""")


def display(i, x, z, info, pesan):
    st.subheader(f"{nama_siswa[i]['nama']} - ({i})")
    st.write(f"- {buku[str(z)]['judul']} **_(ID = {z})_**")
    st.write("Tanggal Peminjaman = ", x[str(z)]["tanggal_peminjaman"])
    if info == 'masa_pinjam':
        st.info(pesan)
    elif info == 'today':
        st.warning(pesan)
    elif info == 'terlambat':
        st.error(pesan)
    st.write(':small_blue_diamond: :small_orange_diamond: ' * 4)


data = open_peminjaman()
nama_siswa = open_siswa()
buku = open_buku()

tab1, tab2, tab3 = st.tabs(["Terlambat", "Dikembalikan Hari Ini", "Masa Peminjaman"])

with tab1:
    cari_info('terlambat')
with tab2:
    cari_info('today')
with tab3:
    cari_info('masa_pinjam')
