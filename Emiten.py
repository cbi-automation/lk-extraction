import re
import importlib

class Emiten:
    def __init__(self, name: str):
        self.name = name
        self.marker_config = {}
        self.marker_to_function = {}
        self.load_emiten_config()

    def load_emiten_config(self):
        """Load konfigurasi marker dan fungsi dari file emiten yang sesuai."""
        try:
            # Mengimport modul berdasarkan nama emiten
            module_name = self.name.upper()
            module = importlib.import_module(module_name)
            
            # Ambil marker_config dan marker_to_function dari modul
            self.marker_config = getattr(module, "marker_config", {})
            self.marker_to_function = getattr(module, "marker_to_function", {})
        except ModuleNotFoundError:
            print(f"[❌] Modul untuk emiten '{self.name}' tidak ditemukan.")
    
    def normalize(self, text):
        """Normalisasi teks untuk menghilangkan spasi berlebih dan lowercase."""
        return re.sub(r"\s+", " ", text.strip().lower())
    
    @abstractmethod
    def find_satuan(self, text, company, kuartal):
        pass

    @abstractmethod
    def find_paragraphs_by_marker_pairs(self, text, kuartal):
        """Metode abstrak untuk mencari teks berdasarkan pasangan marker yang harus diimplementasikan oleh masing-masing emiten."""
        pass
