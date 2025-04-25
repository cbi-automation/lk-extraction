import re
from utils import *

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
tlkm_marker = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("bunga mengambang", "Risiko mata uang asing")]
}


# class TLKM(Emiten):
     
#     marker_to_function = {
#         "marker1": "find_satuan",
#         "marker2": "find_nilai_tukar"
#     }

#     def __init__(self):
#         super().__init__("TLKM")

#     def find_satuan(self, text, company, kuartal):
#         marker_pairs =[("Angka dalam tabel disajikan dalam", ",")]
#         """Contoh fungsi untuk menangani marker 'satuan'."""
#         results = self.find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal)
#         company.disajikan_dalam = results

#     # Seharusnya:
#     def find_nilai_tukar(self, text, company: Company, kuartal: str):
#         marker_pairs = [("Risiko kenaikan nilai tukar mata uang asing", "Risiko harga pasar")]
#         # Gabungkan newline jadi spasi agar regex lebih fleksibel
#         teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal)

#         # Cek apakah teks_kotor adalah list, dan gabungkan menjadi string jika iya
#         if isinstance(teks_kotor, list):
#             teks_kotor = " ".join(teks_kotor)

#         teks_bersih = teks_kotor.replace("\n", " ")

#         # Tangkap pola: mata uang + (penguatan X%) + angka (bisa negatif atau dalam tanda kurung)
#         pola = re.findall(r"(Dolar A\.S\.|Yen Jepang)\s+\(penguatan\s+(\d+%)\)\s+\(?(-?\d+)\)?", teks_bersih)

#         # Inisialisasi variabel hasil
#         perubahan_kurs_usd = None
#         perubahan_kurs_ypg = None
#         ekuitas_usd = None
#         ekuitas_ypg = None

#         for mata_uang, persen, nilai in pola:
#             # Cek apakah nilai aslinya ada dalam tanda kurung
#             match_kurung = re.search(r"\(\s*-?(\d+)\s*\)", text)
#             if match_kurung and match_kurung.group(0) == f"({nilai})":
#                 nilai_bersih = -int(nilai.replace(",", ""))
#             else:
#                 nilai_bersih = int(nilai.replace(",", ""))

#             if mata_uang == "Dolar A.S.":
#                 perubahan_kurs_usd = persen
#                 ekuitas_usd = nilai_bersih
#             elif mata_uang == "Yen Jepang":
#                 perubahan_kurs_ypg = persen
#                 ekuitas_ypg = nilai_bersih

#         company.perubahan_kurs_usd = perubahan_kurs_usd
#         company.perubahan_kurs_ypg = perubahan_kurs_ypg
#         company.ekuitas_usd = ekuitas_usd
#         company.ekuitas_ypg = ekuitas_ypg