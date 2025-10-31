# pedidos/services/excel_report_generator.py
import openpyxl
from django.http import HttpResponse
from .report_generator import ReportGenerator

class ExcelReportGenerator(ReportGenerator):
    """Generador de reportes en formato Excel."""

    def generate(self, pedidos, filename):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Pedidos Pagados"

        ws.append(["ID", "Cliente", "Dirección", "Fecha", "Total", "Estado Pedido", "Productos"])

        for pedido in pedidos:
            productos_str = ", ".join(
                [f"{item.producto} x{item.cantidad}" for item in pedido.items.all()]
            )
            ws.append([
                pedido.id,
                pedido.usuario.nombre,
                getattr(pedido.usuario, "direccion", "N/A"),
                pedido.fecha.strftime("%Y-%m-%d %H:%M"),
                float(pedido.total),
                pedido.estado,
                productos_str
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
        wb.save(response)
        return response
