import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("(Dalam", ",")],
    "marker2": [("Risiko nilai tukar mata uang adalah", "LIPPO KARAWACI")]
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

    # Tangkap persen setelah kata 'Amerika Serikat' atau 'USD'
    persen_match = re.search(r"(?:Amerika Serikat|USD).*?(\d{1,2}%)", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1) if persen_match else "Tidak ditemukan"

    # Tangkap angka Rp setelah frasa "rugi sebelum pajak sebesar" atau langsung setelah 'Rp'
    rupiah_match = re.search(r"(?:rugi sebelum pajak sebesar\s*)?(Rp[\d\.,]+)", teks_bersih, re.IGNORECASE)
    rupiah = rupiah_match.group(1) if rupiah_match else "Tidak ditemukan"

    return {
        'Perubahan Kurs (USD)': persen,
        'Ekuitas/ laba (rugi) (USD)': rupiah
    }
