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

if based_on == 'Penulis':
    for i in options:
        st.subheader(f'Penulis = {i}')
        for x in data_buku:
            if data_buku[x]["penulis"] == i:
                st.write(f'- Judul = {data_buku[x]["judul"]}')
                st.write(f'- ID Buku = {x}')
                st.write(f'- Penerbit = {data_buku[x]["penerbit"]}')
                st.write(f'- Kuantitas = {data_buku[x]["kuantitas"]}')
                st.write(f'- Stock = {buku_stock(x)}')
                st.write(f'- Kategori = {data_buku[x]["kategori"]}')
                st.write("***")

elif based_on == 'Judul Buku':
    for i in options:
        st.subheader(i)
        for x in data_buku:
            if data_buku[x]["judul"] == i:
                st.write(f'- Judul = {data_buku[x]["judul"]}')
                st.write(f'- ID Buku = {x}')
                st.write(f'- Penulis = {data_buku[x]["penulis"]}')
                st.write(f'- Penerbit = {data_buku[x]["penerbit"]}')
                st.write(f'- Kuantitas = {data_buku[x]["kuantitas"]}')
                st.write(f'- Kategori = {data_buku[x]["kategori"]}')
                st.write("***")

elif based_on == 'Penerbit':
    for i in options:
        st.subheader(f'Penerbit = {i}')
        for x in data_buku:
            if data_buku[x]["penerbit"] == i:
                # st.write("***")
                st.write(f'- Judul = {data_buku[x]["judul"]}')
                st.write(f'- ID Buku = {x}')
                st.write(f'- Penulis = {data_buku[x]["penulis"]}')
                st.write(f'- Kuantitas = {data_buku[x]["kuantitas"]}')
                st.write(f'- Kategori = {data_buku[x]["kategori"]}')
                st.write("***")

elif based_on == 'Kategori':
    for i in options:
        st.subheader(f'Kategori = {i}')
        for x in data_buku:
            if data_buku[x]["kategori"] == i:
                # st.write("***")
                st.write(f'- Judul = {data_buku[x]["judul"]}')
                st.write(f'- ID Buku = {x}')
                st.write(f'- Penulis = {data_buku[x]["penulis"]}')
                st.write(f'- Penerbit = {data_buku[x]["penerbit"]}')
                st.write(f'- Kuantitas = {data_buku[x]["kuantitas"]}')
                st.write("***")
