import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("Analisis sensitivitas mata uang asing", "respectively.PT")]
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

    # Cari persentase pelemahan atau penguatan
    persen_match = re.search(r"(?:Pelemahan|Penguatan).*?sebesar\s+(\d+%)", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1) if persen_match else "Tidak ditemukan"

    # Cari angka pertama dalam format RpX (ambil hanya yang pertama)
    rupiah_match = re.search(r"sebesar\s+Rp[\s]?([\d\.,]+)", teks_bersih, re.IGNORECASE)
    rupiah = "Rp" + rupiah_match.group(1) if rupiah_match else "Tidak ditemukan"

    return {
        'Perubahan Kurs (USD)': persen,
        'Ekuitas/ laba (rugi) (USD)': rupiah
    }