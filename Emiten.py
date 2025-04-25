import re
import importlib
from utils import Company

class Emiten(Company):
    def __init__(self, name: str):
        super().__init__(perusahaan=name)  # isi perusahaan di Company
        self.name = name
        self.marker_to_function = {}
        self.load_emiten_config()

    def load_emiten_config(self):
        # load marker or function config here
        pass
   
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
