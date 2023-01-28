import streamlit as st

from pages.const.fun import open_buku, buku_stock

based_on = st.selectbox(
    'Cari dengan',
    ('Judul Buku', 'Penulis', 'Penerbit', 'Kategori')
)

data_buku = open_buku()
pencarian = []
if based_on == 'Judul Buku':
    for i in data_buku:
        pencarian.append(data_buku[i]["judul"])

elif based_on == 'Penulis':
    for i in data_buku:
        pencarian.append(data_buku[i]["penulis"])

elif based_on == 'Penerbit':
    for i in data_buku:
        pencarian.append(data_buku[i]["penerbit"])

elif based_on == 'Kategori':
    for i in data_buku:
        pencarian.append(data_buku[i]["kategori"])

pencarian = list(set(pencarian))
pencarian.sort()

options = st.multiselect(f'Cari berdasarkan {based_on}', pencarian)


def show_cari_buku(search_by):
    st.write(f'- Judul = {data_buku[x]["judul"]}')
    st.write(f'- ID Buku = {x}')
    if search_by != 'penulis':
        st.write(f'- Penulis = {data_buku[x]["penulis"]}')
    if search_by != 'penerbit':
        st.write(f'- Penerbit = {data_buku[x]["penerbit"]}')
    st.write(f'- Kuantitas = {data_buku[x]["kuantitas"]}')
    st.write(f'- Stock = {buku_stock(x)}')
    if search_by != 'kategori':
        st.write(f'- Kategori = {data_buku[x]["kategori"]}')
    st.write("***")


if based_on == 'Penulis':
    for i in options:
        st.subheader(f'Penulis = {i}')
        for x in data_buku:
            if data_buku[x]["penulis"] == i:
                show_cari_buku('penulis')

elif based_on == 'Judul Buku':
    for i in options:
        st.subheader(i)
        for x in data_buku:
            if data_buku[x]["judul"] == i:
                show_cari_buku('')

elif based_on == 'Penerbit':
    for i in options:
        st.subheader(f'Penerbit = {i}')
        for x in data_buku:
            if data_buku[x]["penerbit"] == i:
                show_cari_buku('penerbit')

elif based_on == 'Kategori':
    for i in options:
        st.subheader(f'Kategori = {i}')
        for x in data_buku:
            if data_buku[x]["kategori"] == i:
                show_cari_buku('kategori')
