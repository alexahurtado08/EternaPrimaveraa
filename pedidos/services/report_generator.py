# pedidos/services/report_generator.py
from abc import ABC, abstractmethod

class ReportGenerator(ABC):
    """Interfaz para la generación de reportes."""
    
    @abstractmethod
    def generate(self, data):
        """Genera un reporte a partir de los datos recibidos."""
        pass
