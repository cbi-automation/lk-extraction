import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("meningkat atau menurun", "Risiko harga ekuitas")]
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
    # Gabungkan newline jadi spasi agar regex lebih fleksibel
    # Aktifkan DOTALL agar .* bisa lewati newline
    teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
    teks_bersih = teks_kotor.replace("\n", " ")

   # Tangkap persen: bisa muncul sebelum atau sesudah kata "sebanyak"
    persen_match = re.search(r"(?:sebanyak\s*)?(\d{1,2}%)", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1) if persen_match else "Tidak ditemukan"
    
    # Tangkap nominal: "Rp" atau "USD", diikuti angka dengan titik/koma
    rupiah_match = re.search(r"(Rp|USD)[\s\.]*([\d.,]+)", teks_bersih, re.IGNORECASE)

    if rupiah_match:
        prefix = rupiah_match.group(1)
        nominal = rupiah_match.group(2)
        rupiah = f"{prefix}{nominal}"
    else:
        rupiah = "Tidak ditemukan"

    return {
        'Perubahan Kurs (USD)': persen,
        'Ekuitas/ laba (rugi) (USD)': rupiah
    }