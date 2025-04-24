import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("dinyatakan dalam", ")")],
    "marker2": [("Analisis sensitivitas mata uang asing", "Dampak")]
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
    # Ambil persentase perubahan kurs (contoh: 1,0%)
    teks_kotor = find_paragraphs_by_marker_pairs(text, marker_pairs,kuartal)
    teks_bersih = teks_kotor.replace("\n", " ")

    persen_match = re.search(r"Penguatan\s*([\d.,]+%)", teks_bersih)
    persen = persen_match.group(1) if persen_match else "N/A"

    # Ambil nilai dampak dalam Rupiah (dari baris Penguatan)
    rupiah_match = re.search(r"Penguatan\s*[\d.,]+%\s*\(?([\d.,]+)\)?", teks_bersih)
    rupiah = rupiah_match.group(1) if rupiah_match else "Tidak ditemukan"

    return {
        "Perubahan Kurs (USD)": persen,
        "Ekuitas/ laba (rugi) (USD)": rupiah,
    }
