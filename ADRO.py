import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("jika nilai tukar", "kerugian/keuntungan translasi")]
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

   # Tangkap pola persen di sekitar kata seperti melemah/menguat, strengthened, etc.
    persen_match = re.search(r"(?:melemah/menguat|weakened|strengthened).*?(\d+%)", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1) if persen_match else "Tidak ditemukan"

    # Tangkap nilai lebih rendah
    rendah_match = re.search(r"lebih rendah AS\$([\d\.]+)", teks_bersih)
    lebih_rendah = f"AS${rendah_match.group(1)}" if rendah_match else "Tidak ditemukan"

    # Tangkap nilai lebih tinggi
    tinggi_match = re.search(r"lebih tinggi AS\$([\d\.]+)", teks_bersih)
    lebih_tinggi = f"AS${tinggi_match.group(1)}" if tinggi_match else "Tidak ditemukan"   
    rupiah = rupiah_match.group(1) if rupiah_match else "Tidak ditemukan"

    return {
        "Perubahan Kurs (USD)": f"{persen}",
        "Laba rugi dan ekuitas melemah (USD)": lebih_rendah,
        "Laba rugi dan ekuitas menguat (USD)": lebih_tinggi
    }
