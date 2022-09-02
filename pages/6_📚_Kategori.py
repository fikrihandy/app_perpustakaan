import streamlit as st
from pages.const.fun import open_kategori, save_kategori

col1, col2 = st.columns(2)

kategori = open_kategori()

with col1:
    st.subheader("Kategori")
    st.dataframe(kategori)

with col2:
    st.subheader("Tambah / Hapus Kategori")
    with st.form("Tambah Kategori", True):
        st.write("Tambah Kategori")
        new_kategori = st.text_input("Masukkan nama kategori")
        tambah = st.form_submit_button("Tambah")
        bisa_ditambah = True
        if tambah:
            try:
                for i in kategori["kategori"]:
                    if i == new_kategori:
                        bisa_ditambah = False
                        break
            except KeyError:
                bisa_ditambah = True
            if bisa_ditambah:
                try:
                    new_value = kategori["kategori"]
                    new_value.append(new_kategori)
                    save_kategori({"kategori": new_value})
                except KeyError:
                    kategori = {"kategori": [new_kategori]}
                    save_kategori(kategori)
                st.experimental_rerun()
            else:
                st.warning("Gagal. Kategori tersebut sudah ada.")
    with st.form("Hapus Kategori"):
        st.write("Hapus Kategori")
        try:
            dihapus = st.selectbox('Pilih kategori', kategori["kategori"])
        except KeyError:
            dihapus = st.selectbox('Tidak tersedia', ['No data'])
        hapus = st.form_submit_button("Hapus")
        if hapus:
            try:
                new_value = kategori["kategori"]
                new_value.remove(dihapus)
                save_kategori({"kategori": new_value})
                st.experimental_rerun()
            except KeyError:
                st.error("Tidak dapat dihapus")
