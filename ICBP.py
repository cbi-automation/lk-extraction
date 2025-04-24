import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("menguat", "terutama")]
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

   # Deteksi mata uang pelaporan
    mata_uang_pelaporan = "Rupiah" if "mata uang pelaporan" in teks_bersih.lower() else "Tidak diketahui"

    # Deteksi eksposur terhadap mata uang asing
    if re.search(r'\bUSD|US\$|Dolar AS|United States Dollar\b', teks_bersih, re.IGNORECASE):
        mata_uang_asing = "Dolar AS"
    else:
        mata_uang_asing = "Tidak disebutkan"

    # Ekstrak persentase
    persen_match = re.search(r"menguat/melemah.*?(\d+[.,]?\d*%)", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1).replace(",", ".") if persen_match else "Tidak ditemukan"

    # Ekstrak nominal dalam rupiah
    nominal_match = re.search(r"lebih (?:rendah|tinggi)/(?:tinggi|rendah) sebesar (Rp[\s]*[\d\.]+)", teks_bersih, re.IGNORECASE)
    nominal = nominal_match.group(1).replace(" ", "") if nominal_match else "Tidak ditemukan"

    return {
        "Perubahan Suku Bunga": f"({persen})",
        "Ekuitas/ laba (rugi) (USD)":f"({nominal})"
    }