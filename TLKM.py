import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("Risiko kenaikan nilai tukar mata uang asing", "kenaikan/ penurunan")]
}

def find_satuan(text,marker_pairs,kuartal):
    results = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
    return {
        "satuan": results[0]["snippet"] if results else "-"
    }

def find_nilai_tukar(text, marker_pairs,kuartal):
    # Gabungkan newline jadi spasi agar regex lebih fleksibel
    teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
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

    return {
        "Perubahan Kurs (USD)": perubahan_kurs_usd,
        "Perubahan Kurs (YPG)": perubahan_kurs_ypg,
        "Ekuitas/ laba (rugi) (USD)": ekuitas_usd,
        "Ekuitas/ laba (rugi) (YPG)": ekuitas_ypg,
    }
