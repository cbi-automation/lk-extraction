import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("dinyatakan dalam", ",")],
    "marker2": [("laba konsolidasian Grup", "Risiko harga ekuitas")]
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

     # Deteksi mata uang asing (fokus ke USD)
    if re.search(r'\bUSD|US\$|Dolar AS|United States Dollar\b', teks_bersih, re.IGNORECASE):
        mata_uang_asing = "Dolar AS"
    else:
        mata_uang_asing = "Tidak disebutkan"

    # Ekstrak persentase perubahan kurs USD (misalnya: 0.23% atau 0,23%)
    persen_match = re.search(r"([+-]?\d{1,3}[.,]?\d*)\s*%", teks_bersih)
    persen = persen_match.group(1).replace(",", ".") + "%" if persen_match else "Tidak ditemukan"

    # Ambil hanya angka pertama setelah "tahun berjalan"
    nominal_match = re.search(r"tahun berjalan\s+(\d+)", teks_bersih, re.IGNORECASE)
    nominal = nominal_match.group(1) if nominal_match else "Tidak ditemukan"

    return {
        "Perubahan Suku Bunga": f"({persen})",
        "Ekuitas/ laba (rugi) (USD)":f"({nominal})"
    }