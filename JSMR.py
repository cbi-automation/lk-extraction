import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker3": [("jika nilai tukar", "kerugian/keuntungan translasi")]
}

# Mapping marker ke fungsi
marker_to_function = {
    "marker1": "find_satuan",
    "marker3": "find_suku_bunga"
}

def find_satuan(text,marker_pairs,kuartal):
    results = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
    return {
        "satuan": results[0]["snippet"] if results else "-"
    }


def find_suku_bunga(text, marker_pairs,kuartal):
    teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
    teks_bersih = teks_kotor.replace("\n", " ")

  # Tangkap persen perubahan kurs (bisa 10%, 10.0%, 10,0%)
    persen_match = re.search(r"(?:melemah|menguat|weakened|strengthened).*?(\d+[.,]?\d*)%", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1).replace(",", ".") + "%" if persen_match else "N/A"

    # Tangkap nominal dalam miliar Rupiah (Rp xxx,x atau xxx.x miliar), untuk dua waktu (misal: sekarang dan 31 Desember 2023)
    rupiah_matches = re.findall(r"Rp[\s]*([\d\.,]+)\s*miliar|billion", teks_bersih, re.IGNORECASE)
    rupiah_matches = [r.replace(",", ".") for r in rupiah_matches if r]

    dampak_terbaru = f"Rp {rupiah_matches[0]} miliar" if len(rupiah_matches) > 0 else "N/A"
    dampak_tahun_lalu = f"Rp {rupiah_matches[1]} miliar" if len(rupiah_matches) > 1 else "N/A"

    return {
        "Perubahan Suku Bunga": f"({persen})",
        "Perubahan ekuitas (naik)":f"({lebih_rendah})",
        "Perubahan ekuitas (turun)": f"({lebih_tinggi})",
    }