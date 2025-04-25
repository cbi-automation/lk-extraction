import re
import pdfplumber

atribut_data = ["Kuartal","Ticker","Satuan","Perubahan kurs (USD)","Perubahan kurs (YPG)","Ekuitas/laba(rugi) (USD)","Ekuitas/laba(rugi) (YPG)"]

def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def find_paragraphs_by_marker_pairs(text, marker_pairs, kuartal="2022"):
    text_norm = normalize(text)

    # Ambil pasangan marker pertama saja (karena hanya ada satu)
    start_marker, end_marker = marker_pairs[0]
    start_norm = normalize(start_marker)
    end_norm = normalize(end_marker)

    start_idx = text_norm.find(start_norm)
    if start_idx == -1:
        print(f"[❗] Start marker tidak ditemukan di {kuartal}: {start_marker}")
        return "-"  # Jika tidak ditemukan, kembalikan "-" sebagai indikator tidak ditemukan

    search_range = text_norm[start_idx:]
    end_relative = search_range.find(end_norm)
    if end_relative == -1:
        print(f"[❗] End marker tidak ditemukan setelah start marker di {kuartal}: {end_marker}")
        return "-"  # Jika tidak ditemukan, kembalikan "-" sebagai indikator tidak ditemukan

    end_idx = start_idx + end_relative

    orig_start_idx = text.lower().find(start_marker.lower())
    orig_end_idx = text.lower().find(end_marker.lower(), orig_start_idx)

    if orig_start_idx != -1 and orig_end_idx != -1:
        content_raw = text[orig_start_idx + len(start_marker): orig_end_idx]
        snippet = content_raw.strip()
    else:
        snippet = text_norm[start_idx + len(start_norm): end_idx].strip()

    return snippet  # Kembalikan string langsung, bukan list atau dict

# Mapping marker ke fungsi
marker_to_function = {
    "marker1": "find_satuan",
    "marker2": "find_nilai_tukar"
}

def process_all_markers(text, kuartal, emiten):
    company = Company()
    company.perusahaan = emiten
    company.kuartal = kuartal  # set kuartal langsung
    print(f"[DEBUG] hasil find_satuan untuk {company.kuartal}")


    for marker_name, marker_pairs in marker_config.items():
        function_name = marker_to_function.get(marker_name)
        if not function_name:
            continue

        func = globals().get(function_name)
        if not func:
            print(f"[⚠️] Fungsi '{function_name}' tidak ditemukan.")
            continue

        # ⬇️ Fungsi sekarang juga menerima objek company yang akan di-update
        func(text, marker_pairs, company, kuartal)

    return company

# Fungsi untuk mengekstrak teks dari PDF
def extract_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as doc:
        for page in doc.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Company:
    kuartal: str = "-"
    perusahaan: str = "-"
    disajikan_dalam: str = "-"
    efek_ekuitas: str = "-"
    efek_penurunan_setelah_pajak: str = "-"
    efek_kenaikan_setelah_pajak: str = "-"
    ekuitas_usd: str = "-"
    ekuitas_ypg: str = "-"


# Mapping: atribut class -> nama key di dictionary input
field_map: Dict[str, str] = {
    "kuartal": "Kuartal",
    "perusahaan": "Perusahaan",
    "disajikan_dalam": "Disajikan dalam",
    "efek_penurunan_setelah_pajak": "Efek Penurunan terhadap rugi setelah pajak",
    "efek_kenaikan_setelah_pajak": "Efek Kenaikan terhadap rugi setelah pajak",
    "efek_ekuitas":"Dampak ekuitas (USD)"
}

def get_str(value) -> str:
    if value is None:
        return "-"
    val = str(value).strip()
    return val if val else "-"

def generate_company(doc: Optional[dict]) -> Company:
    data = {}
    for attr, source_key in field_map.items():
        data[attr] = get_str(doc.get(source_key)) if doc else "-"
    return Company(**data)

import json

company = Company()