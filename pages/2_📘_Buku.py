import re
import streamlit as st
from pages.const.fun import open_buku, save_buku, open_kategori, open_peminjaman, buku_stock

tab1, tab2, tab3 = st.tabs(["Daftar Buku", "Tambah Buku", "Hapus Buku"])

with tab1:
    import pandas as pd

    data_buku = open_buku()
    st.header("Database Buku")

    id_ku = []
    judul = []
    penulis = []
    penerbit = []
    kuantitas = []
    stock = []
    kategori = []

    for i in data_buku:
        id_ku.append(i)
        judul.append(data_buku[i]["judul"])
        penulis.append(data_buku[i]["penulis"])
        penerbit.append(data_buku[i]["penerbit"])
        kuantitas.append(data_buku[i]["kuantitas"])
        stock.append(buku_stock(i))
        kategori.append(data_buku[i]["kategori"])

    st.dataframe(pd.DataFrame({
        'ID': id_ku,
        'Judul': judul,
        'Penulis': penulis,
        'Penerbit': penerbit,
        'Kuantitas': kuantitas,
        'Stock': stock,
        'Kategori': kategori
    }))

with tab2:
    with st.form("form", True):
        st.subheader("Tambah Buku ke Database")
        id_buku = st.text_input('ID Buku')
        judul_buku = st.text_input('Judul Buku')
        penulis = st.text_input('Penulis')
        penerbit = st.text_input('Penerbit')
        kuantitas = st.text_input('Kuantitas (Jumlah Buku)')
        try:
            kategori_list = open_kategori()['kategori']
        except KeyError:
            kategori_list = ["-"]
        kategori_tuple = tuple(kategori_list)
        kategori = st.selectbox('Kategori', kategori_tuple)
        submit_tambah = st.form_submit_button("submit")

    if submit_tambah:
        data_buku = open_buku()
        if id_buku in data_buku.keys():
            st.warning("Gagal menambahkan, ID yang sama telah digunakan!", icon="❌")
        else:
            try:
                kuantitas_int = int(kuantitas)
            except (ValueError, TypeError):
                kuantitas_int = 0
            data_buku[id_buku] = {
                "judul": judul_buku,
                "penulis": penulis,
                "penerbit": penerbit,
                "kuantitas": kuantitas_int,
                "kategori": kategori
            }
            sorted_keys = sorted(data_buku.keys())
            data_buku = {key: data_buku[key] for key in sorted_keys}
            save_buku(data_buku)
            st.success(f'Buku = {judul_buku}. Kategori = {kategori}, telah tersimpan')
    else:
        st.info('Data belum disimpan')

with tab3:
    st.subheader("Hapus Buku")
    buku_dict = open_buku()
    buku_list = []
    for value in buku_dict:
        combine_title_id = f'{value} - {buku_dict[value]["judul"]}'
        buku_list.append(combine_title_id)
    buku_list.sort()
    if not buku_list:
        buku_list = ['0 - No data']
    buku_tuple = tuple(buku_list)
    id_buku_str = st.selectbox('ID Buku', buku_tuple)
    id_buku_key = re.findall(r'\d+', id_buku_str)[0]

    if st.button('Hapus'):
        data_buku = open_buku()
        # CEK APAKAH BUKU SEDANG DIPINJAM
        data_peminjaman = open_peminjaman()
        siap_dikembalikan = True
        for i in data_peminjaman:
            for j in data_peminjaman[i]["id"]:
                for key in j:
                    if key == id_buku_key:
                        siap_dikembalikan = False
        if siap_dikembalikan:
            try:
                # HAPUS
                del data_buku[id_buku_key]
                save_buku(data_buku)
                # st.success(f"Buku: {id_buku_str}, telah dihapus")
                st.experimental_rerun()
            except KeyError:
                st.warning("Gagal menghapus buku.")
        else:
            st.warning("Tidak dapat menghapus buku yang sedang dipinjam")
