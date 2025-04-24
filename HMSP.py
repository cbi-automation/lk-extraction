import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("dinyatakan dalam", ",")],
    "marker2": [("menguat/melemah", "higher/lower")]
}

# Mapping marker ke fungsi
marker_to_function = {
    "marker1": "find_satuan",
    "marker2": "find_nilai_tukar"
}

def find_satuan(text,marker_pairs,kuartal):
    results = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
    return {
        "satuan": results[0]["snippet"] if results else "-"
    }

import re

def find_nilai_tukar(text, marker_pairs=None, kuartal=None):
    # Ambil bagian teks yang relevan
    teks_kotor = text if marker_pairs is None else find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal)
    teks_bersih = teks_kotor.replace("\n", " ")

    # Cari perubahan kurs dalam format seperti Rp100/1USD
    kurs_match = re.search(r"(Rp[\d.,]+)\s*/\s*1USD", teks_bersih, re.IGNORECASE)
    kurs = f"{kurs_match.group(1)}/1USD" if kurs_match else "Tidak ditemukan"

    # Cari nilai laba setelah pajak dalam format RpXX miliar (jika ada)
    laba_match = re.search(r"sebesar\s*(Rp[\d.,]+)\s*miliar", teks_bersih, re.IGNORECASE)
    laba = f"{laba_match.group(1)} miliar" if laba_match else "Tidak disebutkan"

    return {
        "Perubahan Kurs (USD)": kurs,
        "Ekuitas/ laba (rugi) (USD)": laba
    }
