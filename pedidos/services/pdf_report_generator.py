# pedidos/services/pdf_report_generator.py
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .report_generator import ReportGenerator

class PDFReportGenerator(ReportGenerator):
    """Generador de reportes en formato PDF."""
    
    def generate(self, template_name, context, filename):
        template = get_template(template_name)
        html = template.render(context)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error al generar el PDF", status=500)
        return response
