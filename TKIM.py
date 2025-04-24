import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", "(")],
    "marker2": [("Risiko nilai tukar mata uang", "increase of approximate")]
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

    persen_match = re.search(r"menguat/melemah.*?(\d+%)", teks_bersih, re.DOTALL)
    persen = persen_match.group(1) if persen_match else "Tidak ditemukan"

    # Tambahkan dukungan angka dengan koma atau titik (contoh: Rp3.223.427 atau Rp3,223,427)
    rupiah_match = re.search(r"lebih tinggi/rendah.*?(Rp[\d\.,]+)", teks_bersih, re.DOTALL)
    rupiah = rupiah_match.group(1) if rupiah_match else "Tidak ditemukan"

    return {
        "Perubahan Kurs (USD)": persen,
        "Ekuitas/ laba (rugi) (USD)": rupiah,
    }
