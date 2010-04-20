from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm, inch, pica

pdf = Canvas("test.pdf", pagesize = letter)
pdf.setFont("Helvetica", 12)
pdf.setStrokeColorRGB(1, 0, 0)
pdf.drawCentredString(letter[0] / 2, inch * 6, "CLASSIFIED")

pdf.showPage()
pdf.save()
