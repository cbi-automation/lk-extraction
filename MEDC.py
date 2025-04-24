import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("tingkat suku bunga pinjaman", "Grup terekspos")]
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


def find_nilai_tukar(text, marker_pairs,kuartal):
    teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
    teks_bersih = teks_kotor.replace("\n", " ")

    # Deteksi perubahan suku bunga (misalnya: 0.5%)
    persen_match = re.search(r"sebesar\s*(\d+[.,]?\d*)%", teks_bersih)
    perubahan_suku_bunga = f"{persen_match.group(1).replace(',', '.')}%" if persen_match else "N/A"

    # Dampak terhadap laba/rugi (ada dua kasus: current & previous)
    dampak_usd = re.findall(r"AS\$([\d.,]+)", teks_bersih)
    dampak_terbaru = f"AS${dampak_usd[0]}" if len(dampak_usd) > 0 else "N/A"

    return {
        "Perubahan Suku Bunga": f"({perubahan_suku_bunga})",
        "Ekuitas/ laba (rugi) (USD)":f"({dampak_terbaru})"
    }