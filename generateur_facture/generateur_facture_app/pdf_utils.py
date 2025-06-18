from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from .models import Factures

def generate_facture_pdf(facture_id):
    # Récupérer la facture
    facture = Factures.objects.get(id=facture_id)
    items = facture.items.all()
    
    # Créer un buffer pour le PDF
    buffer = BytesIO()
    
    # Créer le document PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # En-tête
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 100, f"Facture #{facture.id}")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 120, f"Date: {facture.date_created.strftime('%d/%m/%Y %H:%M')}")
    
    # Détails des produits
    data = [['Produit', 'Prix unitaire', 'Quantité', 'Total']]
    
    for item in items:
        data.append([
            item.Produits.nom,
            f"{item.Produits.prix} €",
            str(item.quantite),
            f"{item.get_prix_total()} €"
        ])
    
    # Total
    data.append(['', '', 'Total:', f"{facture.get_total()} €"])
    
    # Créer le tableau
    table = Table(data, colWidths=[200, 100, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    # Dessiner le tableau
    table.wrapOn(p, width - 200, height)
    table.drawOn(p, 100, height - 300)
    
    # Finaliser le PDF
    p.showPage()
    p.save()
    
    # Récupérer le PDF depuis le buffer
    buffer.seek(0)
    return buffer