from utils import find_paragraphs_by_marker_pairs
import re

# Konfigurasi marker: marker_name -> (start_marker, end_marker)
marker_config = {
    "marker1": [("disajikan dalam", ",")],
    "marker2": [("Risiko kenaikan nilai tukar mata uang asing", "kenaikan/ penurunan")]
}

def find_satuan(text):
    results = find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal)
    return {
        "satuan": results[0]["snippet"] if results else "-"
    }

def find_nilai_tukar(marker_pairs, text, kuartal):
     # Gabungkan newline jadi spasi agar regex lebih fleksibel
    teks_bersih = text.replace("\n", " ")

    # Tangkap pola persen di sekitar kata seperti melemah/menguat, strengthened, etc.
    persen_match = re.search(r"(?:melemah/menguat|weakened|strengthened).*?(\d+%)", teks_bersih, re.IGNORECASE)
    persen = persen_match.group(1) if persen_match else "Tidak ditemukan"

    return {
        "Perubahan Kurs (USD)": perubahan_kurs_usd,
        "Efek Penurunan terhadap rugi setelah pajak (USD)": rugi_turun_usd,
        "Efek Kenaikan terhadap rugi setelah pajak (USD)": rugi_naik_usd,
        "Perubahan Kurs (YPG)": perubahan_kurs_ypg,
        "Efek Penurunan terhadap rugi setelah pajak (YPG)": rugi_turun_ypg,
        "Efek Kenaikan terhadap rugi setelah pajak (YPG)": rugi_naik_ypg,
    }
