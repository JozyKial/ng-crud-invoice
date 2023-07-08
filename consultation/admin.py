from django.contrib import admin
# importation
from .models import *

# Register your models here.
# pour avoir données sous forme de tableau dans Admin
class AdminCustomer(admin.ModelAdmin):
    list_display = ('name_customer','email','phone','address','sexe','age','city','zip_code')
    
class AdminInvoice(admin.ModelAdmin):
    list_display = ('customer','save_by','invoice_date_time','total','last_update_date','paid','invoice_type')

# enregistrement dans admin
admin.site.register(Customer, AdminCustomer)
admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article)
