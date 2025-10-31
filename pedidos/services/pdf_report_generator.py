# Realizado por Alexandra Hurtado y Mariana Valderrama
from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from xhtml2pdf import pisa
from .report_generator import ReportGenerator

class PDFReportGenerator(ReportGenerator):
    """Generador de reportes en formato PDF (traducible)."""
    
    def generate(self, template_name, context, filename):
        template = get_template(template_name)
        html = template.render(context)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            # Mensaje traducible
            return HttpResponse(_("Error al generar el PDF"), status=500)
        return response
