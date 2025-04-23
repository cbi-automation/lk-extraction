import re
import pdfplumber

atribut_data = ["Kuartal","Ticker","Satuan","Perubahan kurs (USD)","Perubahan kurs (YPG)","Ekuitas/laba(rugi) (USD)","Ekuitas/laba(rugi) (YPG)"]

def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())

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

# Mapping marker ke fungsi
marker_to_function = {
    "marker1": "find_satuan",
    "marker2": "find_nilai_tukar",
    "marker3": "find_suku_bunga"
}

def process_all_markers(text, kuartal, marker_config):
    all_output = {}

    for marker_name, marker_pairs in marker_config.items():
        function_name = marker_to_function.get(marker_name)
        if not function_name:
            continue

        func = globals().get(function_name)
        if not func:
            print(f"[⚠️] Fungsi '{function_name}' tidak ditemukan.")
            continue

        output = func(marker_pairs, text, kuartal)
        all_output.update(output)

    return all_output

