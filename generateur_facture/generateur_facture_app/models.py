from django.db import models

class Produits(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_peremption = models.DateField()

    def __str__(self):
        return self.nom

class Factures(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture #{self.id} - {self.date_created.strftime('%Y-%m-%d')}"
    
    def get_total(self):
        return sum(item.get_prix_total() for item in self.items.all())


class Facture_produit(models.Model):
    Factures = models.ForeignKey(Factures, on_delete=models.CASCADE, related_name='items')
    Produits = models.ForeignKey(Produits, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def get_prix_total(self):
        return self.quantite * self.Produits.prix
