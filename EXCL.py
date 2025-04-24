import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("dinyatakan dalam", ",")],
    "marker2": [("melemah/menguat", "kerugian/keuntungan")]
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

    # Ekstrak persen perubahan kurs
    persen_match = re.search(r"(?:melemah/menguat|weakened/strengthened).*?(\d+%)(?=\s)", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1) if persen_match else "Tidak ditemukan"

     # Ambil dua nilai dalam pola 'Rp xx.xxx dan Rp yy.yyy'
    pola = r'Rp\s?([\d\.]+)\s+dan\s+Rp\s?([\d\.]+)'
    hasil = re.search(pola, text)

    nilai_pertama = int(hasil.group(1).replace('.', ''))
    nilai_kedua = int(hasil.group(2).replace('.', ''))

    def format_rp(val):
        return f"Rp{val:,.0f}".replace(",", ".")

    return {
        "Perubahan Kurs (USD)": f"{persen}",
        'Laba rugi dan ekuitas melemah (USD)': f"-{format_rp(nilai_pertama)}",
        'Laba rugi dan ekuitas menguat (USD)': f"+{format_rp(nilai_kedua)}",
    }