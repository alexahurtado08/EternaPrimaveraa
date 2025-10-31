# Realizado por Alexandra Hurtado y Mariana Valderrama
import openpyxl
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .report_generator import ReportGenerator

class ExcelReportGenerator(ReportGenerator):
    """Generador de reportes en formato Excel (traducible)."""

    def generate(self, pedidos, filename):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = _("Pedidos Pagados")  # traducible

        # Encabezados traducibles
        ws.append([
            _("ID"),
            _("Cliente"),
            _("Dirección"),
            _("Fecha"),
            _("Total"),
            _("Estado del Pedido"),
            _("Productos")
        ])

        # Llenado de datos
        for pedido in pedidos:
            productos_str = ", ".join(
                [f"{item.producto} x{item.cantidad}" for item in pedido.items.all()]
            )
            ws.append([
                pedido.id,
                pedido.usuario.nombre,
                getattr(pedido.usuario, "direccion", _("N/A")),
                pedido.fecha.strftime("%Y-%m-%d %H:%M"),
                float(pedido.total),
                pedido.estado,
                productos_str
            ])

        # Configuración de la respuesta HTTP con el archivo Excel
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
        wb.save(response)
        return response
