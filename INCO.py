import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("melemah/menguat", " VALE INDONESIA")]
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

def find_nilai_tukar(text, marker_pairs, kuartal):
    teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal)
    teks_bersih = teks_kotor.replace("\n", " ")

def find_nilai_tukar(teks_bersih, marker_pairs=None, kuartal=None):
    # teks_kotor = text if marker_pairs is None else find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal)
    # teks_bersih = teks_kotor.replace("\n", " ")

    # Tangkap persentase
    persen_match = re.search(r"(?:(?:masing-masing)?\s*sebesar|sebesar|masing-masing)?\s*(\d{1,2}%)", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1) if persen_match else "Tidak ditemukan"

    # Tangkap nominal + simbol + satuan
    rupiah_match = re.search(r"(US\$|Rp)\s*([\d.,]+)\s*(\w+)?", teks_bersih)
    if rupiah_match:
        prefix = rupiah_match.group(1)
        nominal = rupiah_match.group(2)
        satuan = rupiah_match.group(3) or ""
        rupiah = f"{prefix} {nominal} {satuan}".strip()
    else:
        rupiah = "Tidak ditemukan"

    return {
        'Perubahan Kurs (USD)': persen,
        'Ekuitas/ laba (rugi) (USD)': rupiah
    }
