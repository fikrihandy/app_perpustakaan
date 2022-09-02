import re
import time

import streamlit as st

from datetime import datetime
from pages.const.fun import open_siswa, open_peminjaman, open_buku, save_peminjaman

nama_dict = open_siswa()
nama_list = []
for value in nama_dict:
    combine_name_id = f'{nama_dict[value]["nama"]} ({value})'
    nama_list.append(combine_name_id)
nama_list.sort()
if not nama_list:
    nama_list = ['0 - No data']
nama_tuple = tuple(nama_list)
nama = st.selectbox('Nama Siswa', nama_tuple)

data_peminjaman = open_peminjaman()
id_siswa = re.findall(r'\d+', nama)[0]
is_not_zero = True
try:
    for i in data_peminjaman:
        if i == id_siswa:
            is_not_zero = False
            jumlah_dipinjam = len(data_peminjaman[str(i)]["id"])
            st.write(f"Buku yang dipinjam = {jumlah_dipinjam}")
            buku = open_buku()
            for x in data_peminjaman[str(i)]["id"]:
                for z in x:
                    with st.form(z, True):
                        st.subheader(f"{buku[str(z)]['judul']} (ID = {z})")
                        tanggal_kembali = datetime.strptime(x[str(z)]['tanggal_kembali'], '%d/%m/%Y').date()
                        hari_ini = datetime.today().date()
                        delta = hari_ini - tanggal_kembali
                        if tanggal_kembali < hari_ini:
                            st.error(
                                f"⚠️ TERLAMBAT {delta.days} HARI!! 🗓 Tanggal Pengembalian = {x[str(z)]['tanggal_kembali']}")
                        elif tanggal_kembali == hari_ini:
                            st.warning(
                                f"📚 Masa peminjaman berakhir hari ini. ({x[str(z)]['tanggal_kembali']})")
                        elif tanggal_kembali > hari_ini:
                            delta = delta.days * (-1)
                            st.info(
                                f"⏳ Dalam masa peminjaman. Berakhir {delta} hari lagi ({x[str(z)]['tanggal_kembali']}).")
                        st.write("Tanggal Peminjaman = ", x[str(z)]["tanggal_peminjaman"])
                        button_kembalikan = st.form_submit_button(f"Konfirmasi Pengembalian")
                        if button_kembalikan:
                            new_value = data_peminjaman[id_siswa]["id"]
                            for b in new_value:
                                for c in b.keys():
                                    if c == str(z):
                                        new_value.remove(b)
                                        if len(new_value) == 0:
                                            # jika tidak tersedia data hapus dict value (key-data)
                                            del data_peminjaman[id_siswa]
                                        else:
                                            data_peminjaman[id_siswa] = {
                                                "id": new_value
                                            }
                                        save_peminjaman(data_peminjaman)
                            st.success(
                                f"✅ Buku \"{buku[str(z)]['judul']}\", dihapus dari peminjaman.")
                            # EXPERIMENTAL FEATURE! REMOVE IF U WANT
                            with st.spinner("Halaman akan direfresh dalam 5 detik..."):
                                time.sleep(5)
                                st.experimental_rerun()
                    st.write("***")
except RuntimeError:
    st.info("Siswa tidak mempunyai pinjaman buku apapun.")
    st.snow()
if is_not_zero:
    st.warning("🚫 Data peminjaman tidak ditemukan")
