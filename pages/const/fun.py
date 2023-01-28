import json
import sys
import os

my_os = sys.platform
db_list = ["data_buku.json", "data_peminjaman.json", "data_siswa.json", "data_kategori.json"]

db_directory_win32 = os.path.expanduser('~\\.app_perpustakaan')
db_directory_unix = os.path.expanduser("~/.app_perpustakaan")


def kosongan_json_unix(data):
    create_json = open(f"{db_directory_unix}/{data}", 'w')
    create_json.write('{}')
    create_json.close()


def kosongan_json_win32(data):
    create_json = open(f"{db_directory_win32}\\{data}", "w")
    create_json.write('{}')
    create_json.close()


path = ''

# MAC / LINUX
if my_os == "darwin" or my_os == "linux":
    path = db_directory_unix
    if not os.path.isdir(db_directory_unix):
        os.mkdir(os.path.join(os.path.expanduser("~/"), ".app_perpustakaan"))
        # MEMBUAT FILE DB
        for i in db_list:
            kosongan_json_unix(i)
    else:
        for j in db_list:
            # CEK FILE JIKA TIDAK ADA BUAT FILE DB
            is_available = os.path.isfile(f"{db_directory_unix}/{j}")
            if not is_available:
                kosongan_json_unix(j)

# WINDOWS
elif my_os == "win32":
    path = db_directory_win32
    if not os.path.isdir(db_directory_win32):
        os.mkdir(os.path.join(os.path.expanduser("~\\"), ".app_perpustakaan"))
        for i in db_list:
            kosongan_json_win32(i)
    else:
        for j in db_list:
            is_available = os.path.isfile(f"{db_directory_win32}\\{j}")
            if not is_available:
                kosongan_json_win32(j)


# folder tempat database disimpan
# path = '/Users/macbook/Python3Projects/app_perpustakaan/data'


def open_buku():  # buku
    return json.load(open(f'{path}/data_buku.json'))


def save_buku(buku):
    with open(f'{path}/data_buku.json', "w") as outfile:
        json.dump(buku, outfile)


def open_peminjaman():  # peminjaman
    return json.load(open(f'{path}/data_peminjaman.json'))


def save_peminjaman(peminjaman):
    with open(f'{path}/data_peminjaman.json', "w") as outfile:
        json.dump(peminjaman, outfile)


def open_siswa():  # siswa
    return json.load(open(f'{path}/data_siswa.json'))


def save_siswa(siswa):
    with open(f'{path}/data_siswa.json', "w") as outfile:
        json.dump(siswa, outfile)


def open_kategori():  # kategori
    return json.load(open(f'{path}/data_kategori.json'))


def save_kategori(kategori):
    with open(f'{path}/data_kategori.json', "w") as outfile:
        json.dump(kategori, outfile)


def buku_stock(id_buku):
    stock = 0
    data_peminjaman = open_peminjaman()
    data_buku = open_buku()
    for i in data_peminjaman:
        for j in data_peminjaman[i]['id']:
            for key in j:
                if id_buku == key:
                    stock += 1
    return data_buku[id_buku]["kuantitas"] - stock
