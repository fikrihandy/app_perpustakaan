from datetime import date, timedelta
import streamlit as st
import re

from pages.const.fun import open_buku, open_siswa, open_peminjaman, save_peminjaman, buku_stock

st.header('Perpustakaan Ar-Rasyid Wonogiri')
st.subheader('Pinjam Buku')

with st.form("form", True):
    buku_dict = open_buku()
    buku_list = []
    for value in buku_dict:
        combine_title_id = f'{value} - {buku_dict[value]["judul"]}'
        buku_list.append(combine_title_id)
    buku_list.sort()
    buku_tuple = tuple(buku_list)
    id_buku = st.selectbox('ID Buku', buku_tuple)
    nama_dict = open_siswa()
    nama_list = []
    for value in nama_dict:
        combine_name_id = f'{nama_dict[value]["nama"]} ({value})'
        nama_list.append(combine_name_id)
    nama_list.sort()
    nama_tuple = tuple(nama_list)
    nama = st.selectbox('Nama Siswa', nama_tuple)
    submit_pinjam = st.form_submit_button("Pinjam")

    try:
        if submit_pinjam:
            # CEK APAKAH SISWA TERSBUT TELAH MEMINJAM BUKU YANG SAMA ??
            data_peminjaman = open_peminjaman()

            id_regex_nama = re.findall(r'\d+', nama)
            id_siswa = id_regex_nama[0]
            id_regex_title = re.findall(r'\d+', id_buku)
            id_buku = id_regex_title[0]

            siap_dipinjam = True
            pesan = ""

            try:
                for i in data_peminjaman[id_siswa]["id"]:
                    for key in i:
                        if buku_stock(id_buku) <= 0:
                            siap_dipinjam = False
                            pesan = "⚠️ Peminjaman gagal, stock buku tersedia habis."
                        elif key == id_buku:
                            siap_dipinjam = False
                            pesan = "⚠️ Peminjaman gagal, siswa tersebut telah meminjam buku yang sama."
            except KeyError:
                siap_dipinjam = False

            try:
                if len(data_peminjaman[id_siswa]["id"]) >= 3:
                    siap_dipinjam = False
                    pesan = "Melebihi batas maksimum peminjaman."
            except KeyError:
                siap_dipinjam = True

            pinjam = date.today().strftime("%d/%m/%Y")
            kembali = (date.today() + timedelta(7)).strftime("%d/%m/%Y")

            if siap_dipinjam:
                try:
                    new_value = data_peminjaman[id_siswa]["id"]
                    new_value.append({id_buku: {"tanggal_peminjaman": pinjam, "tanggal_kembali": kembali}})
                    data_peminjaman[id_siswa] = {
                        "id": new_value
                    }
                except KeyError:
                    data_peminjaman[id_siswa] = {
                        "id": [
                            {id_buku: {"tanggal_peminjaman": pinjam, "tanggal_kembali": kembali}}
                        ]
                    }

                save_peminjaman(data_peminjaman)
                st.success(f'✅ Peminjaman tercatat.')
            else:
                st.error(pesan)
        else:
            st.warning('Data belum disimpan')
    except TypeError:
        st.error("Kesalahan")

st.write('Pastikan tanggal pada perangkat benar sebelum menggunakan Aplikasi ini!')
st.info(f"Tanggal pada perangkat = {date.today().strftime('%d/%m/%Y')}")
