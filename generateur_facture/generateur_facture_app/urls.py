from django.urls import path
from generateur_facture_app import views

urlpatterns=[
    path('',views.renderDashBoard,name="dashBoard"),
    path('produits/',views.renderProduits,name="produits"),
    path('produits/ajoutProduit/',views.ajoutProduit,name="ajoutProduit"),
    path('produits/modifier/<int:id>/',views.renderModifier,name="modifier"),
    path('produits/modifier/<int:id>/modifProduit/',views.modifProduit,name="modification"),
    path('produits/suprimerProduit/<int:id>/',views.suprimerProduit,name="suprimerProduit"),
    path('produits/rechercheProduit/',views.rechercheProduit,name="recherche"),
    path('creer_facture/', views.creer_facture, name='creer_facture'),
    path('factures/', views.renderFactures, name='factures'),  
    path('factures/suprimerFacture/<int:id>/',views.suprimerFacture,name="suprimerFacture"),
    path('get_facture_details/<int:facture_id>/', views.get_facture_details, name='get_facture_details'),
    path('facture_pdf/<int:facture_id>/', views.facture_pdf, name='facture_pdf'),
]