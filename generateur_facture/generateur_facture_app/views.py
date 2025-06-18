from django.shortcuts import render
from generateur_facture_app.models import Produits,Factures,Facture_produit
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import HttpResponse
from .pdf_utils import generate_facture_pdf
import json


# Create your views here.
def renderDashBoard(request):
    context = {
        'active_page': 'dashboard',
    }
    return render(request, 'dashboard.html', context)


def renderProduits(request):
    produits_list = Produits.objects.all().order_by('id') 
    paginator = Paginator(produits_list, 10)  # 10 produits par page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'active_page': 'produits',
    }
    return render(request, 'Produits.html', context)


def renderModifier(request,id):
    frech=Produits.objects.get(id=id)
    context={
        'frechercher':frech,
        'active_page': 'produits',  # Car c'est lié à la gestion des produits
    }
    return render(request,'modifier.html',context)


def ajoutProduit(request):
    n=request.POST["nom"]
    p=request.POST["prix"]
    d=request.POST["date_peremption"]
    np=Produits(nom=n,prix=p,date_peremption=d)
    np.save()
    return HttpResponseRedirect(reverse("produits"))

def suprimerProduit(request,id):
    psup=Produits.objects.get(id=id)
    psup.delete()
    return HttpResponseRedirect(reverse("produits"))


def modifProduit(request,id):
    # rechercher le tuple dans la bdd
    newId=request.POST["id"]
    oldf=Produits.objects.get(id=newId)
    # remplacement par les nouvelles valeurs
    n=request.POST["nom"]
    p=request.POST["prix"]
    d=request.POST["date_peremption"]
    oldf.nom=n
    oldf.prix=p
    oldf.date_peremption=d
    oldf.save()
    return HttpResponseRedirect(reverse("produits"))

def rechercheProduit(request):
    Id=request.POST["idr"]
    pr=Produits.objects.get(id=Id)
    context={
        'prechercher':pr,
        'active_page': 'produits',
    }
    return render(request,'modifier.html',context)

def creer_facture(request):
    if request.method == 'POST':
        try:
            # Parse les données JSON envoyées
            data = json.loads(request.body)
            produits_data = data.get('produits', [])
            
            if not produits_data:
                return JsonResponse({'success': False, 'error': 'Aucun produit sélectionné'})
            
            # Crée la facture
            nouvelle_facture = Factures.objects.create()
            
            # Ajoute les produits à la facture
            for produit_data in produits_data:
                produit_id = produit_data['produit_id']
                quantite = int(produit_data['quantite'])
                
                produit = Produits.objects.get(id=produit_id)
                Facture_produit.objects.create(
                    Factures=nouvelle_facture,
                    Produits=produit,
                    quantite=quantite
                )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def renderFactures(request):
    factures_list = Factures.objects.all().order_by('-date_created')
    paginator = Paginator(factures_list, 10)  
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'active_page': 'factures',
    }
    return render(request, 'Factures.html', context)

def suprimerFacture(request,id):
    fsup=Factures.objects.get(id=id)
    fsup.delete()
    return HttpResponseRedirect(reverse("factures"))

def get_facture_details(request, facture_id):
    try:
        facture = Factures.objects.get(id=facture_id)
        items = facture.items.all()
        
        data = {
            'facture_id': facture.id,
            'date_created': facture.date_created.strftime("%Y-%m-%d %H:%M"),
            'items': [
                {
                    'produit_nom': item.Produits.nom,
                    'prix': float(item.Produits.prix),
                    'quantite': item.quantite
                }
                for item in items
            ],
            'total': float(facture.get_total())
        }
        return JsonResponse(data)
    except Factures.DoesNotExist:
        return JsonResponse({'error': 'Facture non trouvée'}, status=404)

def facture_pdf(request, facture_id):
    buffer = generate_facture_pdf(facture_id)
    
    # Créer la réponse HTTP
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture_id}.pdf"'
    return response