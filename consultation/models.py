from django.db import models
from django.contrib.auth.models import User


#========== TABLE CUSTOMER (Client)
class Customer(models.Model):
    
    SEXE_TYPE = (
        ('M','Masculin'),
        ('F','Feminin')
    )
    
    name_customer   = models.CharField(max_length=132)
    email           = models.EmailField()
    phone           = models.CharField(max_length=23)
    address         = models.CharField(max_length=100)
    sexe            = models.CharField(max_length=1, choices=SEXE_TYPE)
    age             = models.CharField(max_length=2)
    city            = models.CharField(max_length=32)
    zip_code        = models.CharField(max_length=18)
    created_date    = models.DateTimeField(auto_now_add=True)
    save_by         = models.ForeignKey(User, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        
    def __str__(self):
        return f"{self.name_customer}"


#========== TABLE INVOICE (Facture) : chaque facture doit être liée à un client
class Invoice(models.Model):
    INVOICE_TYPE = (
        ('R','RECU'),
        ('P','PROFORMA FACTURE'),
        ('F','FACTURE')
    )
    
    customer                = models.ForeignKey(Customer, on_delete=models.PROTECT)
    save_by                 = models.ForeignKey(User, on_delete=models.PROTECT)
    invoice_date_time       = models.DateTimeField(auto_now_add=True)
    total                   = models.DecimalField(max_digits=10000, decimal_places=2)
    last_update_date        = models.DateTimeField(null=True, blank=True)
    paid                    = models.BooleanField(default=False)
    invoice_type            = models.CharField(max_length=1, choices=INVOICE_TYPE)
    comments                = models.TextField(null=True, max_length=1000, blank=True)
    
    
    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
    
    def __str__(self):
        return self.customer.name_customer
    
    # calculer le total de la facture
    @property
    def get_total_invoice(self):
        # je récupère d'abord la liste total des articles de la facture
        articles = self.article_set.all()
        # je prends maintenant le prix total
        total = sum(article.get_total_article for article in articles)
        return total


#========== TABLE ARTICLE : les articles sont reliées à une facture
class Article(models.Model):
    invoice         = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name            = models.CharField(max_length=32)
    quantity        = models.IntegerField()
    unit_price      = models.DecimalField(max_digits=1000, decimal_places=2)
    total           = models.DecimalField(max_digits=1000, decimal_places=2)
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        
    #methode pour calculer le total de chaque article
    @property
    def get_total_article(self):
        total = self.quantity * self.unit_price
        return total
    
    