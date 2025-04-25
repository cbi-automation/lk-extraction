import re
import importlib

class Emiten:
    def __init__(self, name: str):
        self.name = name
        self.marker_to_function = {}
        self.load_emiten_config()

   
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
