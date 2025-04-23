from utils import find_paragraphs_by_marker_pairs
import re


def find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal):
    text_norm = normalize(text)
    results = []

    for idx, (start_marker, end_marker) in enumerate(marker_pairs):
        start_norm = normalize(start_marker)
        end_norm = normalize(end_marker)

        start_idx = text_norm.find(start_norm)
        if start_idx == -1:
            print(f"[❗] Start marker tidak ditemukan di {kuartal}: {start_marker}")
            continue

        search_range = text_norm[start_idx:]
        end_relative = search_range.find(end_norm)
        if end_relative == -1:
            print(f"[❗] End marker tidak ditemukan setelah start marker di {kuartal}: {end_marker}")
            continue

        end_idx = start_idx + end_relative

        orig_start_idx = text.lower().find(start_marker.lower())
        orig_end_idx = text.lower().find(end_marker.lower(), orig_start_idx)

        if orig_start_idx != -1 and orig_end_idx != -1:
            content_raw = text[orig_start_idx + len(start_marker): orig_end_idx]
            snippet = content_raw.strip()
            sumber = "Marker Pair (Exact)"
        else:
            snippet = text_norm[start_idx + len(start_norm): end_idx].strip()
            sumber = "Marker Pair (Fallback)"

        # Hasil dikembalikan sebagai dictionary
        results.append({
             "snippet": snippet,
        })

    return results

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
