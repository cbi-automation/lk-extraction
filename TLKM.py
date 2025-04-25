import re
import utils

marker_config = {
    "marker1": [("Angka dalam tabel disajikan dalam", ",")],
    "marker2": [("Risiko kenaikan nilai tukar mata uang asing", "Risiko harga pasar")]
}

# Mapping marker ke fungsi
marker_to_function = {
    "marker1": "find_satuan",
    "marker2": "find_nilai_tukar"
}

def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def find_satuan(text, marker_pairs, company: Company, kuartal: str):
    results = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
    company.disajikan_dalam = results

def find_nilai_tukar(text, marker_pairs, company: Company, kuartal: str):
    # Gabungkan newline jadi spasi agar regex lebih fleksibel
    teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal)

    # Cek apakah teks_kotor adalah list, dan gabungkan menjadi string jika iya
    if isinstance(teks_kotor, list):
        teks_kotor = " ".join(teks_kotor)

    teks_bersih = teks_kotor.replace("\n", " ")

    # Tangkap pola: mata uang + (penguatan X%) + angka (bisa negatif atau dalam tanda kurung)
    pola = re.findall(r"(Dolar A\.S\.|Yen Jepang)\s+\(penguatan\s+(\d+%)\)\s+\(?(-?\d+)\)?", teks_bersih)

    # Inisialisasi variabel hasil
    perubahan_kurs_usd = None
    perubahan_kurs_ypg = None
    ekuitas_usd = None
    ekuitas_ypg = None

    for mata_uang, persen, nilai in pola:
        # Cek apakah nilai aslinya ada dalam tanda kurung
        match_kurung = re.search(r"\(\s*-?(\d+)\s*\)", text)
        if match_kurung and match_kurung.group(0) == f"({nilai})":
            nilai_bersih = -int(nilai.replace(",", ""))
        else:
            nilai_bersih = int(nilai.replace(",", ""))

        if mata_uang == "Dolar A.S.":
            perubahan_kurs_usd = persen
            ekuitas_usd = nilai_bersih
        elif mata_uang == "Yen Jepang":
            perubahan_kurs_ypg = persen
            ekuitas_ypg = nilai_bersih

    company.perubahan_kurs_usd = perubahan_kurs_usd
    company.perubahan_kurs_ypg = perubahan_kurs_ypg
    company.ekuitas_usd = ekuitas_usd
    company.ekuitas_ypg = ekuitas_ypg