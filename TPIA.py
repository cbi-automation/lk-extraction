import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam mata uang", "financial")],
    "marker2": [("Analisis sensitivitas Grup", "turun/naik")]
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

def find_nilai_tukar(teks_bersih):
    # Gabungkan newline jadi spasi agar regex lebih fleksibel
    # teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal)
    # teks_bersih = teks_kotor.replace("\n", " ")

    persen_match = re.search(r"menggunakan.*?(\d+%)", teks_bersih, re.DOTALL)
    persen = persen_match.group(1) if persen_match else "N/A"

    # Cari nilai rugi/laba dalam format US$ xxx ribu
    usd_match = re.search(r"(US\$[\s\d,.]+(?:ribu|thousand)?)", teks_bersih, re.IGNORECASE)
    usd_value = usd_match.group(1).strip() if usd_match else "N/A"

    return {
        "Perubahan Kurs (USD)": persen,
        "Ekuitas/ laba (rugi) (USD)": usd_value,
    }