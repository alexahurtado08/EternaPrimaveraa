# Realizado por Alexandra Hurtado y Mariana Valderrama
from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _

class ReportGenerator(ABC):
    """Interfaz abstracta para la generación de reportes (traducible)."""
    
    @abstractmethod
    def generate(self, data):
        """
        Genera un reporte a partir de los datos recibidos.

        :param data: Datos a incluir en el reporte.
        :type data: iterable o queryset
        :raises NotImplementedError: Si la subclase no implementa este método.
        """
        raise NotImplementedError(_("El método 'generate' debe ser implementado en la subclase."))
