import re
import utils

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", "(")],
    "marker2": [("menguat", "catatan")]
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
    persen = persen_match.group(1) if persen_match else "N/A"

    # Ekstrak nominal dalam juta USD (misalnya: USD74.6 juta dan USD59.1 juta)
    nominal_matches = re.findall(r"USD[\s]*([\d\.,]+)\s*juta|million", teks_bersih)
    nominal_matches = [n.replace(",", ".") for n in nominal_matches if n]  # Normalisasi angka

    lebih_rendah = f"USD{nominal_matches[0]} juta" if len(nominal_matches) > 0 else "N/A"
    lebih_tinggi = f"USD{nominal_matches[1]} juta" if len(nominal_matches) > 1 else "N/A"
    
    return {
        "Perubahan Kurs (USD)": f"{persen}",
        "Laba rugi dan ekuitas melemah (USD)": lebih_rendah,
        "Laba rugi dan ekuitas menguat (USD)": lebih_tinggi
    }