import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("bunga mengambang", "Risiko mata uang asing")]
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

def find_nilai_tukar(text):
    teks_bersih = text.replace("\n", " ")

    # Ambil nilai basis point perubahan USD
    kurs_usd_match = re.search(r"Dolar AS\s*\+(\d+)", teks_bersih)
    perubahan_kurs_usd = f"{kurs_usd_match.group(1)} bps" if kurs_usd_match else "N/A"

    # Ambil nilai dampak USD (angka di baris +100 Dolar AS)
    usd_impact_match = re.search(r"Dolar AS\s*\+\d+\s*\(?([\d.,]+)\)?\s*US Dollar", teks_bersih)
    usd_impact = usd_impact_match.group(1) if usd_impact_match else "Tidak ditemukan"

    # Ambil nilai dampak Rupiah (angka di baris +100 Rupiah)
    rp_impact_match = re.search(r"Rupiah\s*\+\d+\s*\(?([\d.,]+)\)?\s*Rupiah", teks_bersih)
    rp_impact = rp_impact_match.group(1) if rp_impact_match else "Tidak ditemukan"

    return {
        "Perubahan Kurs (USD)": perubahan_kurs_usd,
        "Ekuitas/ laba (rugi) (Rp)": rp_impact,
        "Ekuitas/ laba (rugi) (USD)": usd_impact,
    }