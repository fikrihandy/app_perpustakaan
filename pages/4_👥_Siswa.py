import streamlit as st

from pages.const.fun import open_siswa, save_siswa, open_peminjaman

tab1, tab2, tab3 = st.tabs(["Tambah Siswa", "Hapus Siswa", "Siswa Terdaftar"])

with tab1:
    with st.form("Tambah Siswa", True):
        st.subheader("Tambah Siswa")
        id_siswa = st.text_input('Nomor Identitas Siswa')
        nama_siswa = st.text_input('Nama')

        if st.form_submit_button('Tambahkan'):
            if not (id_siswa.isdigit()) or nama_siswa.isspace() or nama_siswa.isdigit():
                st.warning("Masukkan data dengan benar.", icon="‼️")
            else:
                data_siswa = open_siswa()
                data_siswa[id_siswa] = {
                    "nama": nama_siswa
                }
                save_siswa(data_siswa)
                st.success(f'Saved, Siswa = {nama_siswa} ({id_siswa})')

        else:
            st.info('Data belum disimpan')

with tab2:
    with st.form("Hapus Siswa", True):
        st.subheader("Hapus Siswa")
        id_siswa_remove = st.text_input('Nomor Identitas Siswa', key="remove")
        if st.form_submit_button('Hapus'):
            data_peminjaman = open_peminjaman()
            siap_dihapus = True
            for i in data_peminjaman:
                if i == id_siswa_remove:
                    siap_dihapus = False
                    break
            if siap_dihapus:
                data_siswa = open_siswa()
                try:
                    nama = data_siswa[id_siswa_remove]["nama"]
                    del data_siswa[id_siswa_remove]
                    save_siswa(data_siswa)
                    st.success(f"{nama} (Nomor Identitas = {id_siswa_remove}), telah dihapus dari database.")
                except KeyError:
                    st.warning("Nomor ID tidak diketahui, silahkan periksa kembali")
            else:
                st.warning(f"Konfirmasi pengembalian sebelum menghapus {nama_siswa} dari database")

with tab3:
    import pandas as pd

    data_siswa = open_siswa()
    st.header("Database Siswa")
    no_identitas = []
    nama = []
    for i in data_siswa:
        no_identitas.append(i)
        nama.append(data_siswa[i]["nama"])
    st.dataframe(
        pd.DataFrame(
            {
                # 'ID': no_identitas,
                'Nama Siswa': nama
            }, index=no_identitas
        )
    )
