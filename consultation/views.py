from django.shortcuts import render

#importation
from django.views import View
from .models import *
#from django.contrib.auth.models import User
# importation des messages crées dans settings
from django.contrib import messages
from django.db import transaction

from .utils import pagination

# Create your views here.
class HomeView(View):
    templates_name = 'index.html'
    
    invoices = Invoice.objects.select_related('customer','save_by').all()
    
    context = {
        'invoices':invoices
    }
    
    def get(self, request, *args, **kwargs):    
        items = pagination(request, self.invoices)  
        self.context['invoices'] = items
         
        return render(request,self.templates_name, self.context)
    
    def post(self, request, *args, **kwargs):
        items = pagination(request, self.invoices)  
        self.context['invoices'] = items
        return render(request, self.templates_name, self.context)

""" class pour ajouter un client """
class AddCustomerView(View):
    template_name = 'add_client.html'
    
    # vue qui va se charger d'afficher le template
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    # vu qui va se charger de récupérer les valeurs
    def post(self, request, *args, **kwargs):
        #print(request.POST) teste de récupération
        date = {
            'name_customer'     : request.POST.get('name_customer'),
            'email'             : request.POST.get('email'),
            'phone'             : request.POST.get('phone'),
            'address'           : request.POST.get('address'),
            'sexe'              : request.POST.get('sexe'),
            'age'               : request.POST.get('age'),
            'city'              : request.POST.get('city'),
            'zip_code'          : request.POST.get('zip_code'),
            # récupérer l'utilisateur qui envoi ces données
            'save_by'           : request.user
        }
        
        try:
            created = Customer.objects.create(**date) # les ** c'est pour détaché le dictionnaire des données
            if created:
                messages.success(request, "Le client a été enregistré avec succès.")
            else:
                messages.error(request, "Désolé, veuillez réessayer, les données envoyées ont été corrempue")
        except Exception as e:
            messages.error(request, f"Désolé, notre système a détecté des erreurs {e}")
        
        return render(request, self.template_name)

""" class pour ajouter une facture """
class AddInvoiceView(View):
    template_name = 'add_facture.html'
    
    customers = Customer.objects.select_related('save_by').all()
    
    context = {'customers': customers}
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,self.context)
    
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        items = []
        
        try:
            customer        = request.POST.get('customer')
            type            = request.POST.get('invoice_type')
            articles        = request.POST.getlist('article')
            qtes            = request.POST.getlist('qty')
            units           = request.POST.getlist('unit')
            total_a         = request.POST.getlist('total-a') # total articles
            total           = request.POST.get('total') # le dernier total du formulaire
            comment         = request.POST.get('comment')
            
            invoice_object = {
                'customer_id'   :customer,
                'save_by'       :request.user,
                'total'         :total,
                'invoice_type'  :type,
                'comments'      :comment
            }
            
            invoice = Invoice.objects.create(**invoice_object)
            
            for index, article in enumerate(articles):
                """ [index] : on index le prix concerner car il y on a plusieurs"""
                data = Article(
                    invoice_id  = invoice.id,
                    name        = article,
                    quantity    = qtes[index],
                    unit_price  = units[index], 
                    total       = total_a[index],
                )
                """ on ajoute l'objet data dans la liste items """
                items.append(data)
                """ comme il y a plusieurs objets, on va les créer """
                
            created = Article.objects.bulk_create(items)
            
            if created:
                messages.success(request, "Données enregistrées avec succès.")
            else:
                messages.error(request,"Désolé, veuillez réessayer les données envoyées sont corrompues.")
                
        except Exception as e:
            messages.error(request, f"Sorry the following error has occured {e}.")
        
        return render(request, self.template_name, self.context)
        